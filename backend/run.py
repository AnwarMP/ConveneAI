import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.absolute()
sys.path.append(str(project_root))

import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve
from app import create_app

def print_banner():
    banner = """
 ██████╗ ██████╗ ███╗   ██╗██╗   ██╗███████╗███╗   ██╗███████╗     █████╗ ██╗
██╔════╝██╔═══██╗████╗  ██║██║   ██║██╔════╝████╗  ██║██╔════╝    ██╔══██╗██║
██║     ██║   ██║██╔██╗ ██║██║   ██║█████╗  ██╔██╗ ██║█████╗      ███████║██║
██║     ██║   ██║██║╚██╗██║╚██╗ ██╔╝██╔══╝  ██║╚██╗██║██╔══╝      ██╔══██║██║
╚██████╗╚██████╔╝██║ ╚████║ ╚████╔╝ ███████╗██║ ╚████║███████╗    ██║  ██║██║
 ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝╚══════╝    ╚═╝  ╚═╝╚═╝
                                                                              
██████╗  █████╗  ██████╗██╗  ██╗███████╗███╗   ██╗██████╗ 
██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝████╗  ██║██╔══██╗
██████╔╝███████║██║     █████╔╝ █████╗  ██╔██╗ ██║██║  ██║
██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██║╚██╗██║██║  ██║
██████╔╝██║  ██║╚██████╗██║  ██╗███████╗██║ ╚████║██████╔╝
╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═════╝ 
"""
    version = "v0.1.0"
    print("\033[34m" + banner + "\033[0m")  # Blue color
    print("\033[1m" + f"Version: {version}".center(86) + "\033[0m")  # Bold
    print("\033[1m" + "Starting backend server...".center(86) + "\033[0m\n")  # Bold

asgi_app, flask_app = create_app()

if __name__ == '__main__':
    os.system('clear' if os.name == 'posix' else 'cls')  # Clear screen
    print_banner()
    
    config = Config()
    config.bind = ["0.0.0.0:5000"]
    asyncio.run(serve(asgi_app, config))