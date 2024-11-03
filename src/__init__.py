"""
Source package initialization.
This file marks the src directory as a Python package and provides convenient imports
for commonly used components.
"""

from pathlib import Path

# Define important paths
SRC_ROOT = Path(__file__).parent
PROJECT_ROOT = SRC_ROOT.parent

# Version info
__version__ = "0.1.0"

# Import commonly used components for easier access
from .agent import MeetingAnalysisAgent
from .services.email_service import EmailService

# Define what should be available when someone does 'from src import *'
__all__ = [
    'MeetingAnalysisAgent',
    'EmailService',
    'GeminiAgent'
]