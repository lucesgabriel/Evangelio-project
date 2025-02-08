import os
from termcolor import colored

def check_file(path, description):
    """Check if a file exists and has correct permissions"""
    if os.path.exists(path):
        print(colored(f"✓ {description} found: {path}", "green"))
        return True
    else:
        print(colored(f"✗ {description} not found: {path}", "red"))
        return False

def check_directory(path, description):
    """Check if a directory exists and has correct permissions"""
    if os.path.exists(path) and os.path.isdir(path):
        print(colored(f"✓ {description} found: {path}", "green"))
        return True
    else:
        print(colored(f"✗ {description} not found: {path}", "red"))
        return False

def main():
    print(colored("\nChecking project structure...\n", "yellow"))
    
    # Check main directories
    directories = {
        'src': 'Source directory',
        'src/services': 'Services directory',
        'src/audio': 'Audio directory',
        'src/data': 'Data directory',
        'config': 'Config directory',
        'data/cache': 'Cache directory',
        'data/credentials': 'Credentials directory',
        'audio_files': 'Audio files directory',
        'logs': 'Logs directory'
    }
    
    for dir_path, description in directories.items():
        check_directory(dir_path, description)
    
    # Check critical files
    files = {
        '.env': 'Environment file',
        'config/config.py': 'Configuration file',
        'data/credentials/client-secret.json': 'Google credentials file',
        'main.py': 'Main script',
        'requirements.txt': 'Requirements file'
    }
    
    print(colored("\nChecking critical files...\n", "yellow"))
    for file_path, description in files.items():
        check_file(file_path, description)
    
    # Check Python package structure
    print(colored("\nChecking Python package structure...\n", "yellow"))
    init_files = [
        'src/__init__.py',
        'src/services/__init__.py',
        'src/audio/__init__.py',
        'src/data/__init__.py',
        'config/__init__.py'
    ]
    
    for init_file in init_files:
        check_file(init_file, 'Package __init__ file')

if __name__ == "__main__":
    main() 