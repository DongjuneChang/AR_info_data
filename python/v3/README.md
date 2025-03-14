# TwoBarVisualizer Config Editor v3

A web-based configuration editor for the TwoBarVisualizer in Unity. This editor allows you to modify visualization parameters and save them to GitHub, which will then be applied to the Unity application.

## Features

- **Simple Editor**: Focused interface for editing the three most important parameters:
  - Background Color: Change the color of the visualization background
  - Transparency: Adjust the transparency of the background
  - Distance: Control the distance of the visualization from the camera

- **Advanced Editor**: Full access to all configuration parameters, similar to v2

## Setup

1. Make sure you have Python installed (Python 3.6 or higher recommended)
2. Install the required packages:
   ```
   pip install flask python-dotenv requests
   ```
3. Configure the `.env` file with your GitHub token:
   ```
   GITHUB_TOKEN=your_github_token_here
   ```

## Running the Application

1. Navigate to the v3 directory:
   ```
   cd Assets/Scripts/Task/StepLengthPJT/TwoBarsVIsualizer/python/v3
   ```
2. Run the Flask application:
   ```
   python app.py
   ```
3. Open a web browser and go to:
   ```
   http://localhost:5000
   ```

## Usage

### Simple Editor

The Simple Editor tab provides a streamlined interface for editing the three most important parameters:

1. **Background Color**: Use the color picker to select a color for the background
2. **Transparency**: Adjust the transparency slider to control the opacity of the background
3. **Distance**: Use the position slider to set the distance of the visualization from the camera

Click "Save Changes" to apply your changes to the GitHub repository.

### Advanced Editor

The Advanced Editor tab provides access to all configuration parameters, similar to v2. This includes:

- Display Information
- Bar Style
- Visualizer Settings
- ZeroMQ Settings

Click "Save Changes" to apply your changes to the GitHub repository.

## How It Works

1. The web interface loads the configuration from GitHub
2. You make changes to the configuration using the editor
3. When you save changes, the configuration is updated on GitHub
4. The Unity application loads the updated configuration from GitHub
5. The changes are applied to the ScriptableObjects in Unity

## Technical Details

- The web interface is built with HTML, CSS, and JavaScript
- The backend is built with Flask (Python)
- The configuration is stored in a JSON file on GitHub
- The Unity application uses the TwoBarStepVisualizationConfigManager to apply the configuration to the ScriptableObjects

## Files

- `app.py`: Flask application for serving the web interface and handling API requests
- `schema.json`: JSON Schema for the configuration
- `templates/editor.html`: HTML template for the web interface
- `static/css/styles.css`: CSS styles for the web interface
- `static/js/form-generator.js`: JavaScript for generating forms based on the schema
- `static/js/components/color-picker.js`: Component for selecting colors
- `static/js/components/number-input.js`: Component for numeric input
- `static/js/components/position-control.js`: Component for position control
