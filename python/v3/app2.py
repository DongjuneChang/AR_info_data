#!/usr/bin/env python
from flask import Flask, render_template, jsonify, request, send_from_directory
import json
import os
import base64
import requests
import subprocess
import tempfile
import shutil
from pathlib import Path
from dotenv import load_dotenv

class VisualizerApp:
    """TwoBarVisualizer Application Class - Focused on Overrides"""
    
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize paths
        self.base_path = Path(__file__).parent
        self.config_path = self.base_path / 'config.yaml'
        
        # Load configuration
        self.config = self._load_config()
        
        # GitHub configuration
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.github_owner = os.environ.get('GITHUB_OWNER', 'DongjuneChang')
        self.github_repo = os.environ.get('GITHUB_REPO', 'AR_info_data')
        self.overrides_path = os.environ.get(
            'OVERRIDES_PATH', 
            'visualization/visualization_overrides.json'
        )
        
        # Deploy Key configuration
        self.use_deploy_key = os.environ.get('USE_DEPLOY_KEY', 'false').lower() == 'true'
        self.deploy_key_path = os.environ.get('DEPLOY_KEY_PATH')
        
        # Temporary directory for git operations
        self.temp_dir = None
        if self.use_deploy_key:
            if not self.deploy_key_path:
                print("WARNING: USE_DEPLOY_KEY is true but DEPLOY_KEY_PATH is not set")
            else:
                # Create temporary directory for git operations
                self.temp_dir = tempfile.mkdtemp()
                self._setup_git_repo()
        
        # Initialize Flask app
        self.app = Flask(__name__, 
                        static_folder=self.config['static_path'],
                        template_folder=self.config['templates_path'])
        
        # Register routes
        self._register_routes()

    def _load_config(self):
        """Load YAML configuration file"""
        import yaml
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
            
            # Use Pathlib for path handling
            base_path = Path(config['base_path'])
            config['static_path'] = str(base_path / 'static')
            config['templates_path'] = str(base_path / 'templates')
            
            return config

    def __del__(self):
        """Clean up temporary directory"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def _setup_git_repo(self):
        """Setup git repository with deploy key"""
        try:
            # Clone repository
            repo_url = f"git@github.com:{self.github_owner}/{self.github_repo}.git"
            ssh_command = f"ssh -i {self.deploy_key_path} -o StrictHostKeyChecking=no"
            
            # Set GIT_SSH_COMMAND environment variable
            os.environ["GIT_SSH_COMMAND"] = ssh_command
            
            # Clone repository
            subprocess.run(
                ["git", "clone", repo_url, self.temp_dir],
                check=True,
                capture_output=True
            )
            
            print(f"Successfully cloned repository to {self.temp_dir}")
        except subprocess.CalledProcessError as e:
            print(f"Error setting up git repository: {e.stderr.decode()}")
            if self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
            self.temp_dir = None
    
    def _github_request(self, method, data=None):
        """Handle GitHub API requests"""
        # If using deploy key, use git commands instead of GitHub API
        if self.use_deploy_key and self.temp_dir and method.upper() == 'GET':
            return self._git_get_file()
        elif self.use_deploy_key and self.temp_dir and method.upper() == 'PUT':
            return self._git_put_file(data)
        
        # Otherwise use GitHub API
        headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Add authorization header if token is available
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"
        
        url = f"https://api.github.com/repos/{self.github_owner}/{self.github_repo}/contents/{self.overrides_path}"
        
        if method.upper() == 'GET':
            # For public repos, GET requests don't require a token
            return requests.get(url, headers=headers)
        elif method.upper() == 'PUT':
            if not self.github_token:
                raise ValueError("GitHub token required for PUT requests")
            return requests.put(url, headers=headers, json=data)
        else:
            raise ValueError(f"Unsupported method: {method}")
    
    def _git_get_file(self):
        """Get file using git commands"""
        try:
            # Pull latest changes
            subprocess.run(
                ["git", "pull", "origin", "master"],
                cwd=self.temp_dir,
                check=True,
                capture_output=True
            )
            
            # Read file
            file_path = os.path.join(self.temp_dir, self.overrides_path)
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Create response-like object
            class GitResponse:
                def __init__(self, content):
                    self.status_code = 200
                    self._content = content
                
                def json(self):
                    return {
                        'content': base64.b64encode(self._content.encode()).decode(),
                        'sha': 'git'  # Use 'git' as sha for git operations
                    }
            
            return GitResponse(content)
        except Exception as e:
            # Create error response-like object
            class GitErrorResponse:
                def __init__(self, error):
                    self.status_code = 500
                    self.text = str(error)
            
            return GitErrorResponse(e)
    
    def _git_put_file(self, data):
        """Update file using git commands"""
        try:
            # Write content to file
            file_path = os.path.join(self.temp_dir, self.overrides_path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            print(f"Writing content to {file_path}")
            with open(file_path, 'w') as f:
                content = base64.b64decode(data['content']).decode()
                f.write(content)
                print(f"Content written: {content[:100]}...")
            
            # Commit and push changes
            print("Running git add...")
            add_result = subprocess.run(
                ["git", "add", self.overrides_path],
                cwd=self.temp_dir,
                check=True,
                capture_output=True
            )
            print(f"Git add output: {add_result.stdout.decode()}")
            
            print("Running git commit...")
            commit_message = data.get('message', 'Update visualization overrides')
            commit_result = subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=self.temp_dir,
                check=True,
                capture_output=True
            )
            print(f"Git commit output: {commit_result.stdout.decode()}")
            
            print("Running git push...")
            push_result = subprocess.run(
                ["git", "push", "origin", "master"],
                cwd=self.temp_dir,
                check=False,  # Don't raise exception on error
                capture_output=True
            )
            
            if push_result.returncode != 0:
                print(f"Git push error: {push_result.stderr.decode()}")
                raise Exception(f"Git push failed: {push_result.stderr.decode()}")
            else:
                print(f"Git push output: {push_result.stdout.decode()}")
            
            # Create response-like object
            class GitResponse:
                def __init__(self):
                    self.status_code = 200
                
                def json(self):
                    return {
                        'content': {
                            'sha': 'git'  # Use 'git' as sha for git operations
                        }
                    }
            
            return GitResponse()
        except subprocess.CalledProcessError as e:
            # Create error response-like object
            class GitErrorResponse:
                def __init__(self, error):
                    self.status_code = 500
                    self.text = error.stderr.decode()
            
            return GitErrorResponse(e)

    def _register_routes(self):
        """Register routes"""
        # Main route
        self.app.route('/')(self.overrides_editor)
        
        # API routes
        self.app.route('/overrides', methods=['GET'])(self.get_overrides)
        self.app.route('/overrides', methods=['POST'])(self.update_overrides)
        self.app.route('/color-keys', methods=['GET'])(self.get_color_keys)
        
        # Static files
        self.app.route('/static/<path:filename>')(self.serve_static)

    def overrides_editor(self):
        """Serve overrides editor page"""
        return render_template('overrides.html')

    def get_overrides(self):
        """Get visualization overrides from GitHub or git repository"""
        try:
            response = self._github_request('GET')
            
            if response.status_code != 200:
                return jsonify({
                    'error': 'Failed to fetch overrides',
                    'details': response.text
                }), response.status_code
            
            data = response.json()
            content = base64.b64decode(data['content']).decode('utf-8')
            
            return jsonify({
                'content': content,
                'sha': data['sha']
            })
        except Exception as e:
            return jsonify({
                'error': 'Internal server error',
                'details': str(e)
            }), 500

    def update_overrides(self):
        """Update visualization overrides on GitHub"""
        try:
            print("Received update request")
            data = request.json
            print(f"Request data: {data}")
            
            if not data.get('content') or not data.get('sha'):
                print("Missing required fields")
                return jsonify({
                    'error': 'Missing required fields',
                    'details': 'Both content and sha fields are required'
                }), 400
            
            # Parse and validate the content
            print("Parsing content")
            content_json = json.loads(data['content'])
            print(f"Parsed content: {json.dumps(content_json, indent=2)[:200]}...")
            
            if not isinstance(content_json, dict) or 'visualization_overrides' not in content_json:
                print("Invalid content structure")
                return jsonify({
                    'error': 'Invalid content structure',
                    'details': 'Content must contain visualization_overrides object'
                }), 400
            
            # Validate required fields
            print("Validating required fields")
            required_fields = ['colors', 'centroidPosition', 'enabled']
            for field in required_fields:
                if field not in content_json['visualization_overrides']:
                    print(f"Missing required field: {field}")
                    return jsonify({
                        'error': 'Missing required field',
                        'details': f'Field {field} is required'
                    }), 400
            
            # Validate colors structure
            print("Validating colors structure")
            colors = content_json['visualization_overrides']['colors']
            if not isinstance(colors, dict):
                print("Invalid colors structure")
                return jsonify({
                    'error': 'Invalid colors structure',
                    'details': 'colors must be an object'
                }), 400
            
            # Validate color components
            print("Validating color components")
            for color_key, color_value in colors.items():
                if color_value is not None:
                    for component in ['r', 'g', 'b', 'a']:
                        if component not in color_value or not isinstance(color_value[component], (int, float)):
                            print(f"Invalid {color_key} structure: missing {component}")
                            return jsonify({
                                'error': f'Invalid {color_key} structure',
                                'details': f'{color_key} must contain numeric {component} value'
                            }), 400
            
            # Validate centroidPosition structure
            print("Validating centroidPosition structure")
            pos = content_json['visualization_overrides']['centroidPosition']
            for coord in ['x', 'y', 'z']:
                if coord not in pos or not isinstance(pos[coord], (int, float)):
                    print(f"Invalid centroidPosition structure: missing {coord}")
                    return jsonify({
                        'error': 'Invalid centroidPosition structure',
                        'details': f'centroidPosition must contain numeric {coord} value'
                    }), 400
            
            # Prepare and send update request
            print("Preparing update request")
            payload = {
                "message": "Update visualization overrides",
                "content": base64.b64encode(data['content'].encode()).decode(),
                "sha": data['sha']
            }
            
            print("Sending update request")
            response = self._github_request('PUT', payload)
            
            if response.status_code not in [200, 201]:
                print(f"Error response: {response.status_code} - {response.text}")
                return jsonify({
                    'success': False,
                    'error': f"GitHub API returned status code {response.status_code}",
                    'details': response.text
                })
            
            print("Update successful")
            return jsonify({
                "success": True,
                "message": "Successfully updated visualization overrides"
            })
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return jsonify({
                'error': 'Invalid JSON content',
                'details': str(e)
            }), 400
        except Exception as e:
            print(f"Exception: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'error': 'Internal server error',
                'details': str(e)
            }), 500

    def get_color_keys(self):
        """Get available color keys from visualization overrides"""
        try:
            # First try to get from GitHub
            response = self._github_request('GET')
            
            if response.status_code != 200:
                return jsonify({
                    'error': 'Failed to fetch overrides from GitHub',
                    'details': response.text
                }), response.status_code
            
            data = response.json()
            content = base64.b64decode(data['content']).decode('utf-8')
            content_json = json.loads(content)
            
            if 'visualization_overrides' in content_json and 'colors' in content_json['visualization_overrides']:
                # Get color keys from GitHub
                github_color_keys = list(content_json['visualization_overrides']['colors'].keys())
                
                # Check if barForeground is missing
                if 'barForeground' not in github_color_keys:
                    # Add barForeground to the list
                    github_color_keys.append('barForeground')
                
                return jsonify({
                    'color_keys': github_color_keys
                })
            else:
                return jsonify({
                    'error': 'Invalid JSON structure',
                    'details': 'visualization_overrides.colors not found in JSON'
                }), 400
        except Exception as e:
            return jsonify({
                'error': 'Internal server error',
                'details': str(e)
            }), 500

    def serve_static(self, filename):
        """Serve static files"""
        return send_from_directory(self.app.static_folder, filename)

    def run(self, debug=True, port=5000):
        """Run application"""
        self.app.run(debug=debug, port=port)

if __name__ == '__main__':
    app = VisualizerApp()
    app.run(debug=True, port=5000)
