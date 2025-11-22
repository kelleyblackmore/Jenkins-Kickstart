# Jenkins-Kickstart Usage Guide

## Quick Start

### 1. Install the Package

```bash
pip install jenkins-kickstart
```

### 2. Create a Configuration File

Create a `jenkins-config.yaml` file:

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

### 3. Run Jenkins-Kickstart

```bash
# Validate configuration
jenkins-kickstart jenkins-config.yaml --dry-run

# Test connection
jenkins-kickstart jenkins-config.yaml --test-connection

# Apply configuration
jenkins-kickstart jenkins-config.yaml
```

## Configuration Reference

### Jenkins Connection Settings

```yaml
jenkins:
  # Required: Jenkins server URL
  url: "http://jenkins.example.com:8080"
  
  # Required: Username
  username: "admin"
  
  # Option 1: Use password
  password: "admin123"
  
  # Option 2: Use API token (recommended)
  token: "11234567890abcdef1234567890abcdef"
```

**Getting an API Token:**
1. Log into Jenkins
2. Click your name in the top right → Configure
3. Under API Token, click "Add new Token"
4. Give it a name and click "Generate"
5. Copy the token and use it in your config

### Folder Configuration

Create folders to organize your Jenkins jobs:

```yaml
folders:
  # Root-level folder
  - name: "my-team"
    description: "My team's jobs"
    parent: ""
  
  # Nested folder
  - name: "backend"
    description: "Backend services"
    parent: "my-team"  # Creates my-team/backend
  
  # Deeply nested
  - name: "api"
    description: "API services"
    parent: "my-team/backend"  # Creates my-team/backend/api
```

### Job Configuration

#### Pipeline Job from Git

Pull a Jenkinsfile from a Git repository:

```yaml
jobs:
  - name: "build-app"
    folder: "my-team"
    type: "pipeline"
    description: "Build the application"
    
    # Git settings
    git_url: "https://github.com/user/repo.git"
    git_branch: "*/main"  # Can be */develop, */feature/* etc.
    git_credentials: ""  # Optional: Jenkins credential ID
    
    # Jenkinsfile location in repo
    jenkinsfile: "Jenkinsfile"  # Default path
```

**For Private Repositories:**
```yaml
git_credentials: "github-ssh-key"  # Use credential ID from Jenkins
```

#### Pipeline Job with Inline Script

Define the entire pipeline in the config:

```yaml
jobs:
  - name: "inline-pipeline"
    type: "pipeline"
    description: "Pipeline with inline script"
    script: |
      pipeline {
        agent any
        
        environment {
          APP_NAME = 'my-app'
          VERSION = '1.0.0'
        }
        
        stages {
          stage('Build') {
            steps {
              sh 'echo "Building ${APP_NAME} version ${VERSION}"'
              sh 'make build'
            }
          }
          
          stage('Test') {
            steps {
              sh 'make test'
            }
          }
          
          stage('Deploy') {
            steps {
              sh 'make deploy'
            }
          }
        }
        
        post {
          success {
            echo 'Pipeline succeeded!'
          }
          failure {
            echo 'Pipeline failed!'
          }
        }
      }
```

#### Freestyle Job

Execute shell commands:

```yaml
jobs:
  - name: "deploy-script"
    folder: "my-team"
    type: "freestyle"
    description: "Deploy using shell script"
    commands:
      - "#!/bin/bash"
      - "set -e"
      - "echo 'Starting deployment...'"
      - "./deploy.sh"
      - "echo 'Deployment complete!'"
```

Or as a single command:

```yaml
jobs:
  - name: "simple-task"
    type: "freestyle"
    description: "Run a simple command"
    commands: "echo 'Hello from freestyle job'"
```

## Command-Line Options

### Basic Usage

```bash
jenkins-kickstart <config-file> [options]
```

### Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Validate config without making changes |
| `--test-connection` | Test Jenkins connection only |
| `--verbose` | Show detailed output |
| `--help` | Show help message |

### Examples

```bash
# Validate configuration syntax
jenkins-kickstart config.yaml --dry-run

# Test if Jenkins is reachable
jenkins-kickstart config.yaml --test-connection

# Apply configuration with verbose output
jenkins-kickstart config.yaml --verbose

# Quick validation
jenkins-kickstart config.yaml --dry-run
```

## Python API

### Basic Usage

```python
from jenkins_kickstart import JenkinsKickstart, ConfigParser

# Load configuration
config = ConfigParser('config.yaml')

# Validate configuration
config.validate()

# Create Jenkins client
client = JenkinsKickstart(
    url='http://localhost:8080',
    username='admin',
    token='your-api-token'
)

# Test connection
if client.test_connection():
    # Setup Jenkins
    client.setup_from_config(config)
```

### Manual Folder/Job Creation

```python
from jenkins_kickstart import JenkinsKickstart

client = JenkinsKickstart(
    url='http://localhost:8080',
    username='admin',
    token='your-api-token'
)

# Create a folder
client.create_folder(
    name='my-folder',
    description='My folder description'
)

# Create a nested folder
client.create_folder(
    name='subfolder',
    description='Nested folder',
    parent='my-folder'
)

# Create a pipeline job
job_config = {
    'type': 'pipeline',
    'description': 'My pipeline job',
    'script': '''
        pipeline {
            agent any
            stages {
                stage('Build') {
                    steps {
                        echo 'Building...'
                    }
                }
            }
        }
    '''
}

client.create_job('my-job', job_config, folder='my-folder')
```

## Troubleshooting

### Connection Issues

**Problem:** Cannot connect to Jenkins

**Solutions:**
1. Verify Jenkins URL is correct and accessible
2. Check if Jenkins is running: `curl http://localhost:8080`
3. Verify username and credentials
4. Check if authentication is required
5. Try using `--test-connection` to diagnose

### Authentication Errors

**Problem:** 401 Unauthorized or 403 Forbidden

**Solutions:**
1. Use API token instead of password
2. Verify username is correct
3. Check user has necessary permissions
4. In Jenkins: Manage Jenkins → Configure Global Security → ensure API token is enabled

### Folder/Job Already Exists

**Behavior:** Jenkins-Kickstart will detect existing folders/jobs and skip creation

**Output:**
```
Folder already exists: my-folder
Job already exists: my-folder/my-job
```

This is normal behavior - the tool is idempotent.

### Configuration Validation Errors

**Problem:** Configuration validation fails

**Common issues:**
1. Missing required fields (url, username)
2. Invalid YAML/JSON syntax
3. Wrong file extension (.yaml, .yml, or .json required)

**Debug:**
```bash
jenkins-kickstart config.yaml --dry-run --verbose
```

### Plugin Requirements

Some features require Jenkins plugins:

- **Folders:** CloudBees Folders Plugin
- **Pipeline:** Pipeline Plugin
- **Git:** Git Plugin

Most of these are included in standard Jenkins installations.

## Best Practices

### 1. Use API Tokens

Always prefer API tokens over passwords:

```yaml
jenkins:
  username: "admin"
  token: "1234567890abcdef..."  # Not password
```

### 2. Version Control Your Configs

Store your configuration files in Git:

```bash
git add jenkins-config.yaml
git commit -m "Add Jenkins configuration"
```

### 3. Use Dry-Run First

Always validate before applying:

```bash
jenkins-kickstart config.yaml --dry-run
jenkins-kickstart config.yaml  # Apply after validation
```

### 4. Organize with Folders

Use folders to organize jobs by team, environment, or project:

```yaml
folders:
  - name: "team-a"
  - name: "team-b"
  - name: "production"
  - name: "staging"
```

### 5. Keep Secrets Secure

Don't commit credentials to Git. Use environment variables:

```yaml
jenkins:
  url: "${JENKINS_URL}"
  username: "${JENKINS_USER}"
  token: "${JENKINS_TOKEN}"
```

Or use a secrets file (add to .gitignore):

```yaml
# jenkins-config.yaml (in Git)
jenkins:
  url: "http://localhost:8080"

# jenkins-secrets.yaml (in .gitignore)
jenkins:
  username: "admin"
  token: "secret-token"
```

### 6. Test on Non-Production First

Test your configuration on a development Jenkins instance before applying to production.

## Examples

See the `examples/` directory for complete configuration examples:

- `minimal-config.yaml` - Simplest possible configuration
- `example-config.yaml` - Common use cases
- `advanced-config.yaml` - Advanced features and patterns
- `example-config.json` - JSON format example

## Support

For issues or questions:
- GitHub Issues: https://github.com/kelleyblackmore/Jenkins-Kickstart/issues
- Documentation: https://github.com/kelleyblackmore/Jenkins-Kickstart
