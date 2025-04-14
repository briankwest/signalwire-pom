"""
Helper script for Windows installations.
This script installs an alias for pom_tool using a .bat file.
"""
import os
import sys
import shutil

def install_windows_bat():
    """Create a .bat file for Windows users"""
    python_path = sys.executable
    scripts_dir = os.path.join(os.path.dirname(os.path.dirname(python_path)), 'Scripts')
    
    # Ensure the directory exists
    os.makedirs(scripts_dir, exist_ok=True)
    
    # Create the .bat file
    bat_path = os.path.join(scripts_dir, 'pom_tool.bat')
    
    with open(bat_path, 'w') as f:
        f.write('@echo off\r\n')
        f.write(f'"{python_path}" -m signalwire_pom.cli %*\r\n')
    
    print(f"Created Windows batch file at: {bat_path}")
    return True

if __name__ == "__main__":
    install_windows_bat() 