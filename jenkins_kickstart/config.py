"""
Configuration file parser for Jenkins-Kickstart
"""

import yaml
import json
from typing import Dict, Any, List
from pathlib import Path


class ConfigParser:
    """Parser for Jenkins configuration files (YAML or JSON)"""
    
    def __init__(self, config_path: str):
        """
        Initialize the config parser
        
        Args:
            config_path: Path to the configuration file
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            if self.config_path.suffix in ['.yaml', '.yml']:
                return yaml.safe_load(f)
            elif self.config_path.suffix == '.json':
                return json.load(f)
            else:
                raise ValueError(f"Unsupported file format: {self.config_path.suffix}")
    
    def get_jenkins_url(self) -> str:
        """Get Jenkins URL from config"""
        return self.config.get('jenkins', {}).get('url', '')
    
    def get_jenkins_credentials(self) -> Dict[str, str]:
        """Get Jenkins credentials from config"""
        jenkins_config = self.config.get('jenkins', {})
        return {
            'username': jenkins_config.get('username', ''),
            'password': jenkins_config.get('password', ''),
            'token': jenkins_config.get('token', '')
        }
    
    def get_folders(self) -> List[Dict[str, Any]]:
        """Get folder configurations"""
        return self.config.get('folders', [])
    
    def get_jobs(self) -> List[Dict[str, Any]]:
        """Get job configurations"""
        return self.config.get('jobs', [])
    
    def validate(self) -> bool:
        """Validate configuration structure"""
        required_keys = ['jenkins']
        for key in required_keys:
            if key not in self.config:
                raise ValueError(f"Missing required configuration key: {key}")
        
        jenkins_config = self.config.get('jenkins', {})
        if not jenkins_config.get('url'):
            raise ValueError("Jenkins URL is required")
        
        return True
