"""
Jenkins-Kickstart: A Python package to kickstart Jenkins configuration
"""

__version__ = "0.1.0"

from .client import JenkinsKickstart
from .config import ConfigParser

__all__ = ["JenkinsKickstart", "ConfigParser"]
