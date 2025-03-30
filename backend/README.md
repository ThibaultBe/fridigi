# Python Virtual Environment Cheatsheet

This cheatsheet provides quick reference commands for creating, activating, and managing Python virtual environments (venv), along with pip package management.

## Creating a Virtual Environment

```bash
# Create a virtual environment in the current directory
python -m venv venv

# Create a virtual environment in a specific location
python -m venv /path/to/venv

# Create with specific Python version (if you have multiple installed)
python3.9 -m venv venv
```

## Activating the Virtual Environment

### On Windows:

```bash
# Command Prompt
venv\Scripts\activate.bat

# PowerShell
venv\Scripts\Activate.ps1
```

### On macOS and Linux:

```bash
source venv/bin/activate
```

Once activated, you should see the environment name in your terminal prompt like:

```
(venv) $
```

## Deactivating the Virtual Environment

From any platform, when the environment is active, simply run:

```bash
deactivate
```

## Managing Pip

```bash
# Check pip version
pip --version

# Update pip itself
pip install --upgrade pip

# Install packages from requirements.txt
pip install -r requirements.txt

# Generate a requirements.txt file
pip freeze > requirements.txt
```

## Additional Useful Commands

```bash
# List all installed packages in the environment
pip list

# Install a specific package
pip install package_name

# Install a specific package version
pip install package_name==1.2.3

# Uninstall a package
pip uninstall package_name
```

## Best Practices

1. Always activate the virtual environment before installing packages
2. Include a requirements.txt file with your project
3. Avoid using global pip installations for project dependencies
4. Update your requirements.txt after adding new dependencies
