# TwoBarsVisualizer Refactoring Details

## 1. Class Structure

```python
class VisualizerApp:
    """TwoBarVisualizer Application Class"""
    
    def __init__(self):
        # Initialize configuration
        pass
        
    def _load_config(self):
        """Load configuration file"""
        pass
        
    def _load_schema(self):
        """Load schema file"""
        pass
        
    def _register_routes(self):
        """Register routes"""
        pass
        
    # Route handlers
    
    def run(self, debug=True, port=5000):
        """Run application"""
        pass
```

## 2. Configuration Improvement

### Current config.yaml
```yaml
base_path: D:/Data_AR/Test_ws2/asu-tele-rehab-ar-robotics/Assets/Scripts/Task/StepLengthPJT/TwoBarsVIsualizer/python/v3
static_path: ${base_path}/static
templates_path: ${base_path}/templates
```

### Improved config.yaml
```yaml
static_path: static
templates_path: templates
```

## 3. Environment Variables

Required environment variables:
- `GITHUB_TOKEN`: GitHub API access token
- `GITHUB_OWNER`: GitHub repository owner (default: "DongjuneChang")
- `GITHUB_REPO`: GitHub repository name (default: "AR")
- `CONFIG_PATH`: Configuration file path (default: "AR_info_data/visualization/two_bar_step_visualization_config.json")
- `OVERRIDES_PATH`: Overrides file path (default: "AR_info_data/visualization/visualization_overrides.json")

## 4. Key Method Implementations

### Configuration Loading
```python
def _load_config(self):
    """Load YAML configuration file"""
    with open(self.config_path, 'r') as f:
        config = yaml.safe_load(f)
        
        # Handle relative paths
        base_path = Path(__file__).parent
        config['static_path'] = str(base_path / config.get('static_path', 'static'))
        config['templates_path'] = str(base_path / config.get('templates_path', 'templates'))
        
        return config
```

### GitHub API Request Handling
```python
def _github_request(self, method, path, data=None):
    """Handle GitHub API requests"""
    headers = {
        "Authorization": f"token {self.github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    url = f"https://api.github.com/repos/{self.github_owner}/{self.github_repo}/contents/{path}"
    
    if method.upper() == 'GET':
        return requests.get(url, headers=headers)
    elif method.upper() == 'PUT':
        return requests.put(url, headers=headers, json=data)
    else:
        raise ValueError(f"Unsupported method: {method}")
```

### Key Parameter Extraction
```python
def _extract_key_parameters(self):
    """Extract key parameters from schema"""
    key_params = []
    
    def search_schema(schema_part, path="", in_properties=False):
        if isinstance(schema_part, dict):
            if schema_part.get('x-key-parameter') == True:
                display_name = schema_part.get('x-display-name', path.split('.')[-1])
                key_params.append({
                    'path': path,
                    'display_name': display_name,
                    'schema': schema_part
                })
            
            for key, value in schema_part.items():
                if key == 'properties':
                    search_schema(value, path, True)
                else:
                    new_path = f"{path}.{key}" if path else key
                    search_schema(value, new_path, in_properties)
    
    if 'properties' in self.schema:
        for key, value in self.schema['properties'].items():
            search_schema(value, key)
    
    return key_params
```

## 5. Route Handler Implementation

Each route handler will be converted from existing functions to class methods.

## 6. Main Execution Code

```python
if __name__ == '__main__':
    app = VisualizerApp()
    app.run(debug=True, port=5000)
```

## 7. Virtual Environment Setup

### PowerShell Commands
```powershell
# Activate virtual environment
cd D:\Data_AI\AutoTrading\env312
.\Scripts\Activate.ps1

# Install required packages
pip install flask python-dotenv pyyaml requests jsonschema

# Run the application
python path\to\app2.py
```

## 8. Code Cleanup Strategy

1. Remove unnecessary print statements
2. Extract duplicate code into methods
3. Apply consistent error handling
4. Use clear variable names
5. Add documentation for better code understanding

## 9. Testing Plan

1. Test in virtual environment
2. Verify all routes work correctly
3. Check GitHub integration
4. Validate configuration handling
5. Test error scenarios
