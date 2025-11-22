# Jenkins-Kickstart

A Python package to kickstart Jenkins configuration after an instance is up. Configure Jenkins folders, settings, and jobs using a simple configuration file that interacts with the Jenkins API.

## Features

- **Automated Jenkins Setup**: Configure your Jenkins instance from a YAML or JSON file
- **Folder Management**: Create and organize Jenkins folders with custom settings
- **Job Creation**: Set up Jenkins jobs (Pipeline and Freestyle) with just a few lines of configuration
- **Git Integration**: Configure pipeline jobs to pull from Git repositories with Jenkinsfiles
- **Inline Scripts**: Define pipeline scripts directly in the configuration file
- **CLI Interface**: Easy-to-use command-line tool for quick setup
- **Validation**: Built-in configuration validation before making changes

## Installation

### From Source

```bash
git clone https://github.com/kelleyblackmore/Jenkins-Kickstart.git
cd Jenkins-Kickstart
pip install -e .
```

### From PyPI (when published)

```bash
pip install jenkins-kickstart
```

## Quick Start

1. **Create a configuration file** (`my-jenkins-config.yaml`):

```yaml
jenkins:
  url: "http://localhost:8080"
  username: "admin"
  password: "admin"

folders:
  - name: "my-project"
    description: "My project jobs"

jobs:
  - name: "hello-world"
    folder: "my-project"
    type: "pipeline"
    description: "A simple hello world job"
    script: |
      pipeline {
        agent any
        stages {
          stage('Hello') {
            steps {
              echo 'Hello, World!'
            }
          }
        }
      }
```

2. **Run Jenkins-Kickstart**:

```bash
jenkins-kickstart my-jenkins-config.yaml
```

## Usage

### Command Line Interface

```bash
# Setup Jenkins from config file
jenkins-kickstart config.yaml

# Test connection without making changes
jenkins-kickstart config.yaml --test-connection

# Validate configuration without connecting
jenkins-kickstart config.yaml --dry-run

# Verbose output
jenkins-kickstart config.yaml --verbose
```

### Python API

```python
from jenkins_kickstart import JenkinsKickstart, ConfigParser

# Load configuration
config = ConfigParser('config.yaml')

# Initialize Jenkins client
client = JenkinsKickstart(
    url='http://localhost:8080',
    username='admin',
    password='admin'
)

# Test connection
if client.test_connection():
    # Setup Jenkins from config
    client.setup_from_config(config)
```

## Configuration File Format

### Basic Structure

```yaml
jenkins:
  url: "http://your-jenkins-url:8080"
  username: "your-username"
  password: "your-password"  # or use token
  # token: "your-api-token"   # preferred over password

folders:
  - name: "folder-name"
    description: "Folder description"
    parent: ""  # parent folder path, empty for root

jobs:
  - name: "job-name"
    folder: "folder-name"  # optional, empty for root
    type: "pipeline"  # or "freestyle"
    description: "Job description"
    # ... additional job-specific settings
```

### Folder Configuration

```yaml
folders:
  # Root level folder
  - name: "development"
    description: "Development environment"
    parent: ""
  
  # Nested folder
  - name: "backend"
    description: "Backend services"
    parent: "development"  # creates development/backend
```

### Pipeline Job from Git

```yaml
jobs:
  - name: "my-pipeline"
    folder: "development"
    type: "pipeline"
    description: "Build from Git repository"
    git_url: "https://github.com/user/repo.git"
    git_branch: "*/main"
    git_credentials: "github-credentials-id"  # optional
    jenkinsfile: "Jenkinsfile"  # path in repo
```

### Pipeline Job with Inline Script

```yaml
jobs:
  - name: "inline-pipeline"
    type: "pipeline"
    description: "Pipeline with inline script"
    script: |
      pipeline {
        agent any
        stages {
          stage('Build') {
            steps {
              sh 'make build'
            }
          }
          stage('Test') {
            steps {
              sh 'make test'
            }
          }
        }
      }
```

### Freestyle Job

```yaml
jobs:
  - name: "freestyle-job"
    type: "freestyle"
    description: "Freestyle job with shell commands"
    commands:
      - "echo 'Starting build...'"
      - "npm install"
      - "npm run build"
      - "npm test"
```

## Examples

See the `examples/` directory for more configuration examples:

- `example-config.yaml` - Comprehensive example with various job types
- `example-config.json` - JSON format configuration
- `minimal-config.yaml` - Minimal working configuration

## Requirements

- Python 3.7+
- Jenkins server with API access
- Jenkins user account with appropriate permissions

## Dependencies

- `python-jenkins` - Jenkins API client
- `pyyaml` - YAML configuration parsing
- `requests` - HTTP library

## Authentication

Jenkins-Kickstart supports two authentication methods:

1. **Username/Password**: Basic authentication
2. **Username/Token**: API token (recommended for security)

To generate an API token in Jenkins:
1. Go to your user profile
2. Click "Configure"
3. Under "API Token", click "Add new Token"
4. Copy the generated token and use it in your config

## Use Cases

- **New Jenkins Instances**: Quickly set up a new Jenkins server with your standard configuration
- **Disaster Recovery**: Restore Jenkins configuration from a backup config file
- **Environment Replication**: Duplicate Jenkins setup across dev/staging/production
- **Team Onboarding**: Share Jenkins configuration as code with team members
- **CI/CD Automation**: Integrate into infrastructure-as-code workflows

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.