"""
Main Jenkins client for kickstarting configuration
"""

import jenkins
import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Optional
from pathlib import Path


class JenkinsKickstart:
    """Main client for managing Jenkins configuration"""
    
    def __init__(self, url: str, username: str = '', password: str = '', token: str = ''):
        """
        Initialize Jenkins client
        
        Args:
            url: Jenkins server URL
            username: Jenkins username
            password: Jenkins password (or token)
            token: Jenkins API token (preferred over password)
        """
        self.url = url.rstrip('/')
        auth_token = token if token else password
        self.server = jenkins.Jenkins(url, username=username, password=auth_token)
        
    def test_connection(self) -> bool:
        """Test connection to Jenkins server"""
        try:
            user = self.server.get_whoami()
            version = self.server.get_version()
            print(f"Connected to Jenkins {version} as {user.get('fullName', 'Unknown')}")
            return True
        except Exception as e:
            print(f"Failed to connect to Jenkins: {e}")
            return False
    
    def create_folder(self, name: str, description: str = '', parent: str = '') -> bool:
        """
        Create a folder in Jenkins
        
        Args:
            name: Folder name
            description: Folder description
            parent: Parent folder path (empty for root)
            
        Returns:
            True if successful, False otherwise
        """
        folder_path = f"{parent}/{name}" if parent else name
        
        # Check if folder already exists
        if self.folder_exists(folder_path):
            print(f"Folder already exists: {folder_path}")
            return True
        
        # Create folder XML config
        folder_config = f'''<?xml version='1.1' encoding='UTF-8'?>
<com.cloudbees.hudson.plugins.folder.Folder plugin="cloudbees-folder">
  <description>{description}</description>
  <properties/>
  <folderViews class="com.cloudbees.hudson.plugins.folder.views.DefaultFolderViewHolder">
    <views>
      <hudson.model.AllView>
        <owner class="com.cloudbees.hudson.plugins.folder.Folder" reference="../../../.."/>
        <name>All</name>
        <filterExecutors>false</filterExecutors>
        <filterQueue>false</filterQueue>
        <properties class="hudson.model.View$PropertyList"/>
      </hudson.model.AllView>
    </views>
    <tabBar class="hudson.views.DefaultViewsTabBar"/>
  </folderViews>
  <healthMetrics/>
  <icon class="com.cloudbees.hudson.plugins.folder.icons.StockFolderIcon"/>
</com.cloudbees.hudson.plugins.folder.Folder>'''
        
        try:
            self.server.create_job(folder_path, folder_config)
            print(f"Created folder: {folder_path}")
            return True
        except Exception as e:
            print(f"Failed to create folder {folder_path}: {e}")
            return False
    
    def folder_exists(self, folder_path: str) -> bool:
        """Check if a folder exists"""
        try:
            self.server.get_job_config(folder_path)
            return True
        except jenkins.NotFoundException:
            return False
        except Exception:
            return False
    
    def create_job(self, name: str, config: Dict[str, Any], folder: str = '') -> bool:
        """
        Create a Jenkins job
        
        Args:
            name: Job name
            config: Job configuration dictionary
            folder: Folder path (empty for root)
            
        Returns:
            True if successful, False otherwise
        """
        job_path = f"{folder}/{name}" if folder else name
        
        # Check if job already exists
        if self.job_exists(job_path):
            print(f"Job already exists: {job_path}")
            return True
        
        # Generate job XML based on config
        job_xml = self._generate_job_xml(config)
        
        try:
            self.server.create_job(job_path, job_xml)
            print(f"Created job: {job_path}")
            return True
        except Exception as e:
            print(f"Failed to create job {job_path}: {e}")
            return False
    
    def job_exists(self, job_path: str) -> bool:
        """Check if a job exists"""
        try:
            self.server.get_job_config(job_path)
            return True
        except jenkins.NotFoundException:
            return False
        except Exception:
            return False
    
    def _generate_job_xml(self, config: Dict[str, Any]) -> str:
        """Generate Jenkins job XML from configuration"""
        job_type = config.get('type', 'pipeline')
        
        if job_type == 'pipeline':
            return self._generate_pipeline_job_xml(config)
        elif job_type == 'freestyle':
            return self._generate_freestyle_job_xml(config)
        else:
            raise ValueError(f"Unsupported job type: {job_type}")
    
    def _generate_pipeline_job_xml(self, config: Dict[str, Any]) -> str:
        """Generate pipeline job XML"""
        description = config.get('description', '')
        jenkinsfile = config.get('jenkinsfile', 'Jenkinsfile')
        git_url = config.get('git_url', '')
        git_branch = config.get('git_branch', '*/main')
        git_credentials = config.get('git_credentials', '')
        
        # Build script source - either from SCM or inline script
        if git_url:
            script_source = f'''<definition class="org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition" plugin="workflow-cps">
      <scm class="hudson.plugins.git.GitSCM" plugin="git">
        <configVersion>2</configVersion>
        <userRemoteConfigs>
          <hudson.plugins.git.UserRemoteConfig>
            <url>{git_url}</url>
            {f'<credentialsId>{git_credentials}</credentialsId>' if git_credentials else ''}
          </hudson.plugins.git.UserRemoteConfig>
        </userRemoteConfigs>
        <branches>
          <hudson.plugins.git.BranchSpec>
            <name>{git_branch}</name>
          </hudson.plugins.git.BranchSpec>
        </branches>
        <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
        <submoduleCfg class="empty-list"/>
        <extensions/>
      </scm>
      <scriptPath>{jenkinsfile}</scriptPath>
      <lightweight>true</lightweight>
    </definition>'''
        else:
            # Inline script
            script = config.get('script', 'echo "Hello from Jenkins"')
            script_source = f'''<definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps">
      <script>{script}</script>
      <sandbox>true</sandbox>
    </definition>'''
        
        return f'''<?xml version='1.1' encoding='UTF-8'?>
<flow-definition plugin="workflow-job">
  <description>{description}</description>
  <keepDependencies>false</keepDependencies>
  <properties/>
  {script_source}
  <triggers/>
  <disabled>false</disabled>
</flow-definition>'''
    
    def _generate_freestyle_job_xml(self, config: Dict[str, Any]) -> str:
        """Generate freestyle job XML"""
        description = config.get('description', '')
        commands = config.get('commands', [])
        command_string = '\n'.join(commands) if isinstance(commands, list) else commands
        
        return f'''<?xml version='1.1' encoding='UTF-8'?>
<project>
  <description>{description}</description>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <scm class="hudson.scm.NullSCM"/>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers/>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <hudson.tasks.Shell>
      <command>{command_string}</command>
    </hudson.tasks.Shell>
  </builders>
  <publishers/>
  <buildWrappers/>
</project>'''
    
    def setup_from_config(self, config_parser) -> bool:
        """
        Setup Jenkins from a configuration parser
        
        Args:
            config_parser: ConfigParser instance
            
        Returns:
            True if all operations successful
        """
        success = True
        
        # Create folders
        folders = config_parser.get_folders()
        for folder_config in folders:
            name = folder_config.get('name')
            description = folder_config.get('description', '')
            parent = folder_config.get('parent', '')
            
            if not self.create_folder(name, description, parent):
                success = False
        
        # Create jobs
        jobs = config_parser.get_jobs()
        for job_config in jobs:
            name = job_config.get('name')
            folder = job_config.get('folder', '')
            
            if not self.create_job(name, job_config, folder):
                success = False
        
        return success
