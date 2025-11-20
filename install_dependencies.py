#!/usr/bin/env python3

"""
Script to install all dependencies for the 5G Core Management Prototype
"""

import subprocess
import sys
import os

def install_python_packages():
    """Install Python packages"""
    print("Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("Python dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing Python dependencies: {e}")
        return False
    return True

def install_netconf_dependencies():
    """Install NETCONF server dependencies"""
    print("Installing NETCONF server dependencies...")
    try:
        os.chdir("netconf")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        os.chdir("..")
        print("NETCONF server dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing NETCONF server dependencies: {e}")
        os.chdir("..")
        return False
    except FileNotFoundError:
        print("NETCONF requirements.txt not found")
        os.chdir("..")
        return False
    return True

def install_restconf_dependencies():
    """Install RESTCONF server dependencies"""
    print("Installing RESTCONF server dependencies...")
    try:
        os.chdir("restconf")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        os.chdir("..")
        print("RESTCONF server dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing RESTCONF server dependencies: {e}")
        os.chdir("..")
        return False
    except FileNotFoundError:
        print("RESTCONF requirements.txt not found")
        os.chdir("..")
        return False
    return True

def install_snmp_dependencies():
    """Install SNMP agent dependencies"""
    print("Installing SNMP agent dependencies...")
    try:
        os.chdir("snmp")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        os.chdir("..")
        print("SNMP agent dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing SNMP agent dependencies: {e}")
        os.chdir("..")
        return False
    except FileNotFoundError:
        print("SNMP requirements.txt not found")
        os.chdir("..")
        return False
    return True

def check_nodejs():
    """Check if Node.js is installed"""
    print("Checking for Node.js...")
    try:
        subprocess.run(["node", "--version"], check=True, stdout=subprocess.DEVNULL)
        print("Node.js is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Node.js not found. Please install Node.js to run the web dashboard")
        return False

def check_docker():
    """Check if Docker is installed"""
    print("Checking for Docker...")
    try:
        subprocess.run(["docker", "--version"], check=True, stdout=subprocess.DEVNULL)
        print("Docker is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Docker not found. Please install Docker to run Open5GS")
        return False

def main():
    print("5G Core Management Prototype - Dependency Installation")
    print("=" * 50)
    
    # Check prerequisites
    node_available = check_nodejs()
    docker_available = check_docker()
    
    # Install Python dependencies
    if not install_python_packages():
        print("Failed to install main Python dependencies")
        return
    
    if not install_netconf_dependencies():
        print("Failed to install NETCONF dependencies")
        return
    
    if not install_restconf_dependencies():
        print("Failed to install RESTCONF dependencies")
        return
    
    if not install_snmp_dependencies():
        print("Failed to install SNMP dependencies")
        return
    
    print("\n" + "=" * 50)
    print("Dependency installation completed!")
    print("\nTo run the prototype:")
    if docker_available:
        print("- Use 'docker-compose up -d' to start Open5GS")
    else:
        print("- Install Docker to run Open5GS")
    
    if node_available:
        print("- Use 'cd web-dashboard && npm install && npm start' to start the web dashboard")
    else:
        print("- Install Node.js to run the web dashboard")
    
    print("- Use 'python netconf/netconf_server.py' to start the NETCONF server")
    print("- Use 'python restconf/restconf_server.py' to start the RESTCONF server")
    print("- Use 'python snmp/snmp_agent.py' to start the SNMP agent")
    print("- Use 'python run_all.py' to start all components together")

if __name__ == "__main__":
    main()