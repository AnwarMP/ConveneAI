"""
Backend package initialization.
This file marks the backend directory as a Python package and can contain package-level configuration.
"""

from pathlib import Path

# Define important paths
BACKEND_ROOT = Path(__file__).parent
PROJECT_ROOT = BACKEND_ROOT.parent

# Version info
__version__ = "0.1.0"

# Package level constants
API_PREFIX = "/api/v1"
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 5000

# You can add more package-level configuration here