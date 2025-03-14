#!/usr/bin/env python
from flask import Flask, render_template, jsonify, request, send_from_directory
import json
import os
import base64
import requests
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
        self.github_repo = os.environ.get('GITHUB_REPO', 'AR')
        self.overrides_path = os.environ.get(
            'OVERRIDES_PATH', 
            'AR_info_data/visualization/visualization_overrides.json'
        )
        
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

    def _github_request(self, method, data=None):
        """Handle GitHub API requests"""
        if not self.github_token:
            raise ValueError("GitHub token not found in environment variables")
            
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        url = f"https://api.github.com/repos/{self.github_owner}/{self.github_repo}/contents/{self.overrides_path}"
        
        if method.upper() == 'GET':
            return requests.get(url, headers=headers)
        elif method.upper() == 'PUT':
            return requests.put(url, headers=headers, json=data)
        else:
            raise ValueError(f"Unsupported method: {method}")

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
        """Get visualization overrides from GitHub"""
        try:
            response = self._github_request('GET')
            
            if response.status_code != 200:
                return jsonify({
                    'error': 'Failed to fetch overrides from GitHub',
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
            data = request.json
            
            if not data.get('content') or not data.get('sha'):
                return jsonify({
                    'error': 'Missing required fields',
                    'details': 'Both content and sha fields are required'
                }), 400
            
            # Parse and validate the content
            content_json = json.loads(data['content'])
            if not isinstance(content_json, dict) or 'visualization_overrides' not in content_json:
                return jsonify({
                    'error': 'Invalid content structure',
                    'details': 'Content must contain visualization_overrides object'
                }), 400
            
            # Validate required fields
            required_fields = ['colors', 'centroidPosition', 'enabled']
            for field in required_fields:
                if field not in content_json['visualization_overrides']:
                    return jsonify({
                        'error': 'Missing required field',
                        'details': f'Field {field} is required'
                    }), 400
            
            # Validate colors structure
            colors = content_json['visualization_overrides']['colors']
            if not isinstance(colors, dict):
                return jsonify({
                    'error': 'Invalid colors structure',
                    'details': 'colors must be an object'
                }), 400
            
            # Validate color components
            for color_key, color_value in colors.items():
                if color_value is not None:
                    for component in ['r', 'g', 'b', 'a']:
                        if component not in color_value or not isinstance(color_value[component], (int, float)):
                            return jsonify({
                                'error': f'Invalid {color_key} structure',
                                'details': f'{color_key} must contain numeric {component} value'
                            }), 400
            
            # Validate centroidPosition structure
            pos = content_json['visualization_overrides']['centroidPosition']
            for coord in ['x', 'y', 'z']:
                if coord not in pos or not isinstance(pos[coord], (int, float)):
                    return jsonify({
                        'error': 'Invalid centroidPosition structure',
                        'details': f'centroidPosition must contain numeric {coord} value'
                    }), 400
            
            # Prepare and send update request
            payload = {
                "message": "Update visualization overrides",
                "content": base64.b64encode(data['content'].encode()).decode(),
                "sha": data['sha']
            }
            
            response = self._github_request('PUT', payload)
            
            if response.status_code not in [200, 201]:
                return jsonify({
                    'success': False,
                    'error': f"GitHub API returned status code {response.status_code}",
                    'details': response.text
                })
            
            return jsonify({
                "success": True,
                "message": "Successfully updated visualization overrides"
            })
        except json.JSONDecodeError as e:
            return jsonify({
                'error': 'Invalid JSON content',
                'details': str(e)
            }), 400
        except Exception as e:
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
