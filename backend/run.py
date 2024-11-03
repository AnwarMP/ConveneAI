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

asgi_app, flask_app = create_app()

if __name__ == '__main__':
    config = Config()
    config.bind = ["0.0.0.0:5000"]
    asyncio.run(serve(asgi_app, config))