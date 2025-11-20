#!/usr/bin/env python3
"""
Setup and run script for 5G Core Management System
"""

import subprocess
import sys
import os

def check_and_install_package(package_name, import_name=None):
    """Check if a package is installed, install if not"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✓ {package_name} is already installed")
        return True
    except ImportError:
        print(f"✗ {package_name} not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"✓ {package_name} installed successfully")
            return True
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {package_name}")
            return False

def main():
    print("=" * 60)
    print("5G Core Management System - Setup and Run")
    print("=" * 60)
    
    # Required packages
    packages = [
        ("ncclient", "ncclient"),
        ("flask", "flask"),
        ("lxml", "lxml"),
        ("pyang", "pyang"),
        ("pysnmp", "pysnmp"),
        ("pyasn1", "pyasn1"),
        ("requests", "requests"),
    ]
    
    print("\n1. Checking and installing dependencies...")
    all_installed = True
    for package, import_name in packages:
        if not check_and_install_package(package, import_name):
            all_installed = False
    
    if not all_installed:
        print("\n⚠ Some packages failed to install. Please install manually:")
        print("   python -m pip install ncclient flask lxml pyang pysnmp pyasn1 requests")
        return
    
    print("\n2. All dependencies are ready!")
    print("\n3. Starting NETCONF/RESTCONF Server...")
    print("   (Press Ctrl+C to stop)")
    print("-" * 60)
    
    # Change to the netconf server directory
    server_path = os.path.join("5g-core-management", "management-plane", "netconf-server", "netconf_server.py")
    
    if not os.path.exists(server_path):
        print(f"✗ Server file not found: {server_path}")
        return
    
    try:
        # Start the server
        os.chdir(os.path.dirname(server_path))
        subprocess.run([sys.executable, "netconf_server.py"])
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except Exception as e:
        print(f"\n✗ Error starting server: {e}")

if __name__ == "__main__":
    main()

