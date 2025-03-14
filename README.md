# AR Information Data

This repository contains configuration and information data for ASU AR applications, specifically focused on the Tele-Rehab AR project. The repository serves as a central location for configuration files that can be accessed and modified by both the Unity AR application and web-based configuration tools.

## Repository Purpose

The main purpose of this repository is to:
1. Store configuration files for AR visualization components
2. Provide a way to update these configurations at runtime
3. Enable web-based editing of visualization parameters
4. Maintain device-specific settings and ROS integration information

## Structure

- `startup.json`: Main startup configuration for the AR application
- `devices/`: Device-specific configuration files for different HoloLens and desktop devices
- `images/`: Reference images and visual resources
- `ros_info/`: ROS-related configuration and data for robot integration
- `visualization/`: Visualization settings and configurations
  - `two_bar_step_visualization_config.json`: Base configuration for two-bar step visualization with reference line and area settings
  - `visualization_overrides.json`: Runtime overrides for visualization settings
  - `step_trigger_config.json`: Configuration for step trigger functionality
- `python/`: Web-based configuration tools
  - `v3/`: Latest version of the web configuration editor
    - `app2.py`: Flask application for serving the web interface
    - `config.yaml`: Configuration for the web application
    - `static/`: Static assets (CSS, JavaScript, images)
    - `templates/`: HTML templates for the web interface

## Web Configuration Tool

The repository includes a web-based configuration tool in the `python/v3` directory. This tool allows you to:

1. View and edit visualization parameters through a user-friendly interface
2. Save changes directly to this GitHub repository
3. Apply changes to the AR application at runtime

### Setting Up the Web Tool

The web tool can use either GitHub Deploy Keys (recommended) or Personal Access Tokens for authentication:

#### Option 1: Using Deploy Keys (Recommended)

1. **Generate an SSH key pair**:
   ```bash
   ssh-keygen -t ed25519 -C "ar_info_data_editor"
   # Save to a secure location, e.g., ~/.ssh/ar_info_data_key
   ```

2. **Add the public key as a Deploy Key**:
   - Go to the GitHub repository settings
   - Navigate to "Deploy keys" > "Add deploy key"
   - Paste the content of the public key (`.pub` file)
   - Check "Allow write access" if you need to update files
   - Save the key

3. **Configure the web tool**:
   - Create a `.env` file in the `python/v3` directory based on `.env.example`
   - Set `USE_DEPLOY_KEY=true`
   - Set `DEPLOY_KEY_PATH` to the path of your private key
   - Update other settings as needed

#### Option 2: Using Personal Access Token

1. **Generate a GitHub Personal Access Token**:
   - Go to GitHub Settings > Developer settings > Personal access tokens
   - Generate a new token with `repo` scope
   - Copy the token

2. **Configure the web tool**:
   - Create a `.env` file in the `python/v3` directory based on `.env.example`
   - Set `GITHUB_TOKEN` to your personal access token
   - Update other settings as needed

### Running the Web Tool

To run the web configuration tool:

```bash
cd python/v3
python app2.py
```

Then open a web browser and navigate to `http://localhost:5000`.

## Unity Integration

The Unity AR application loads configuration files from this repository at startup and can also check for updates during runtime. The `TwoBarStepVisualizationConfigManager.cs` script handles loading and applying these configurations to the appropriate ScriptableObjects.

## Reference Line and Area Visualization

The visualization configuration includes settings for reference lines and areas:

- **Reference Line**: A horizontal line that can be displayed at a specific value
  - Configured in `visualization/two_bar_step_visualization_config.json`
  - Can be overridden at runtime via `visualization/visualization_overrides.json`

- **Reference Area**: A shaded area between minimum and maximum values
  - Configured in `visualization/two_bar_step_visualization_config.json`
  - Can be overridden at runtime via `visualization/visualization_overrides.json`

## Usage

These configuration files are used by the ASU Tele-Rehab AR application to customize various components and behaviors. The web configuration tool provides an easy way to modify these settings without having to edit JSON files directly.

## For Lab Members

To get access to the Deploy Key for editing configurations, please contact the lab administrator. The Deploy Key allows you to update the configuration files through the web interface without needing to create a personal GitHub token.
