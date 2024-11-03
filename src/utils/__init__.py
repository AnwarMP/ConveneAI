"""
Utilities package initialization.
Contains utility classes and helper functions for email analysis and context management.

Classes:
    EmailQueryGenerator: Generates Gmail search queries from analyzed transcripts
    ContextProvider: Provides contextual information like dates and times
"""

from .query_generator import EmailQueryGenerator
from .context_provider import ContextProvider

# Define which classes/functions should be available when using 'from src.utils import *'
__all__ = [
    'EmailQueryGenerator',
    'ContextProvider'
]

# Version tracking
__version__ = '0.1.0'

# Commonly used instances
default_query_generator = EmailQueryGenerator()
context_provider = ContextProvider()

# Helper function for easy access to current context
def get_current_context():
    """Get the current date and time context"""
    return context_provider.get_current_context()

# Export helper functions as well
__all__ += ['get_current_context']