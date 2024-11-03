import os
import sys
from pathlib import Path

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        'flask',
        'python-dotenv',
        'hypercorn',
        'asgiref',
        'llama-index-llms-anthropic'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing required packages. Installing...")
        os.system(f"pip install {' '.join(missing_packages)}")
    else:
        print("All required packages are installed.")

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_path = Path('.env')
    
    if not env_path.exists():
        print("Creating .env file...")
        with open(env_path, 'w') as f:
            f.write("ANTHROPIC_API_KEY=your_key_here\n")
        print("Please edit .env file and add your Anthropic API key")
        return False
    
    return True

def check_directory_structure():
    """Check if all required directories and files exist"""
    required_structure = {
        'backend/app': ['__init__.py', 'routes.py'],
        'backend/config': ['__init__.py'],
        'backend': ['run.py'],
        'src/services': ['email_service.py'],
        'src/utils': ['query_generator.py'],
        'src': ['agent.py']
    }
    
    missing_items = []
    for directory, files in required_structure.items():
        dir_path = Path(directory)
        if not dir_path.exists():
            missing_items.append(f"Directory: {directory}")
            continue
        
        for file in files:
            file_path = dir_path / file
            if not file_path.exists():
                missing_items.append(f"File: {directory}/{file}")
    
    return missing_items

def main():
    """Main setup function"""
    print("Starting setup...")
    
    # Check dependencies
    check_dependencies()
    
    # Check directory structure
    missing_items = check_directory_structure()
    if missing_items:
        print("\nMissing required files/directories:")
        for item in missing_items:
            print(f"- {item}")
        print("\nPlease ensure all required files are present before running the application.")
        sys.exit(1)
    
    # Check .env file
    if not check_env_file():
        print("Please add your Anthropic API key to the .env file before running the application.")
        sys.exit(1)
    
    print("\nSetup complete! You can now run the application with:")
    print("python backend/run.py")

if __name__ == "__main__":
    main()