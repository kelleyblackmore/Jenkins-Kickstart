"""
Command-line interface for Jenkins-Kickstart
"""

import argparse
import sys
from .config import ConfigParser
from .client import JenkinsKickstart


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Jenkins-Kickstart: Kickstart Jenkins configuration from a config file'
    )
    
    parser.add_argument(
        'config',
        help='Path to the configuration file (YAML or JSON)'
    )
    
    parser.add_argument(
        '--test-connection',
        action='store_true',
        help='Test connection to Jenkins server without making changes'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Parse config and validate without making changes'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    try:
        # Load and validate configuration
        print(f"Loading configuration from: {args.config}")
        config_parser = ConfigParser(args.config)
        config_parser.validate()
        print("Configuration validated successfully")
        
        if args.dry_run:
            print("\nDry run mode - no changes will be made")
            print(f"Jenkins URL: {config_parser.get_jenkins_url()}")
            print(f"Folders to create: {len(config_parser.get_folders())}")
            print(f"Jobs to create: {len(config_parser.get_jobs())}")
            return 0
        
        # Initialize Jenkins client
        jenkins_url = config_parser.get_jenkins_url()
        creds = config_parser.get_jenkins_credentials()
        
        print(f"\nConnecting to Jenkins at: {jenkins_url}")
        client = JenkinsKickstart(
            url=jenkins_url,
            username=creds.get('username', ''),
            password=creds.get('password', ''),
            token=creds.get('token', '')
        )
        
        # Test connection
        if not client.test_connection():
            print("ERROR: Failed to connect to Jenkins")
            return 1
        
        if args.test_connection:
            print("Connection test successful!")
            return 0
        
        # Setup Jenkins from config
        print("\nSetting up Jenkins configuration...")
        if client.setup_from_config(config_parser):
            print("\nJenkins kickstart completed successfully!")
            return 0
        else:
            print("\nJenkins kickstart completed with some errors")
            return 1
            
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"ERROR: Configuration validation failed: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
