#!/usr/bin/env python3

"""
Main script to run all 5G Core Management components
"""

import subprocess
import sys
import time
import threading
import os

def run_command(command, name):
    """Run a command in a subprocess and print its output"""
    try:
        print(f"Starting {name}...")
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Print output in real-time
        if process.stdout:
            for line in process.stdout:
                print(f"[{name}] {line.strip()}")
            
        process.wait()
        print(f"{name} finished with exit code {process.returncode}")
    except Exception as e:
        print(f"Error running {name}: {e}")

def main():
    print("Starting 5G Core Management Prototype...")
    print("This will start all components: Open5GS, NETCONF Server, RESTCONF Server, SNMP Agent, and Web Dashboard")
    print("Press Ctrl+C to stop all services")
    
    # Start Open5GS using Docker Compose
    print("\n1. Starting Open5GS with Docker Compose...")
    try:
        subprocess.run(["docker-compose", "up", "-d"], check=True)
        print("Open5GS started successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error starting Open5GS: {e}")
        return
    except FileNotFoundError:
        print("Docker Compose not found. Please install Docker and Docker Compose.")
        return
    
    # Wait a bit for Open5GS to start
    time.sleep(10)
    
    # Start NETCONF server
    print("\n2. Starting NETCONF Server...")
    netconf_thread = threading.Thread(
        target=run_command,
        args=("python netconf/netconf_server.py", "NETCONF Server")
    )
    netconf_thread.daemon = True
    netconf_thread.start()
    
    # Start RESTCONF server
    print("\n3. Starting RESTCONF Server...")
    restconf_thread = threading.Thread(
        target=run_command,
        args=("python restconf/restconf_server.py", "RESTCONF Server")
    )
    restconf_thread.daemon = True
    restconf_thread.start()
    
    # Start SNMP agent
    print("\n4. Starting SNMP Agent...")
    snmp_thread = threading.Thread(
        target=run_command,
        args=("python snmp/snmp_agent.py", "SNMP Agent")
    )
    snmp_thread.daemon = True
    snmp_thread.start()
    
    # Start Web Dashboard
    print("\n5. Starting Web Dashboard...")
    try:
        # Change to web-dashboard directory and install dependencies
        os.chdir("web-dashboard")
        subprocess.run(["npm", "install"], check=True)
        print("Web Dashboard dependencies installed")
        
        # Start the dashboard server
        dashboard_thread = threading.Thread(
            target=run_command,
            args=("npm start", "Web Dashboard")
        )
        dashboard_thread.daemon = True
        dashboard_thread.start()
        
        # Change back to parent directory
        os.chdir("..")
    except subprocess.CalledProcessError as e:
        print(f"Error setting up Web Dashboard: {e}")
    except FileNotFoundError:
        print("Node.js/npm not found. Please install Node.js to run the Web Dashboard.")
    
    print("\nAll components started!")
    print("\nAccess the components at:")
    print("- Open5GS: http://localhost:3000 (Web UI)")
    print("- RESTCONF API: http://localhost:8081/restconf")
    print("- SNMP Agent: localhost:161")
    print("- Web Dashboard: http://localhost:3000")
    print("\nPress Ctrl+C to stop all services")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down all services...")
        # Stop Docker containers
        try:
            subprocess.run(["docker-compose", "down"], check=True)
            print("Open5GS stopped")
        except subprocess.CalledProcessError as e:
            print(f"Error stopping Open5GS: {e}")
        
        print("All services stopped. Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()