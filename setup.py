from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jenkins-kickstart",
    version="0.1.0",
    author="Jenkins-Kickstart Contributors",
    description="A Python package to kickstart Jenkins configuration after instance setup",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kelleyblackmore/Jenkins-Kickstart",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "python-jenkins>=1.7.0",
        "pyyaml>=5.4",
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "jenkins-kickstart=jenkins_kickstart.cli:main",
        ],
    },
)
