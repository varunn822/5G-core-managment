#!/usr/bin/env python3
"""
Script to start all 5G Core Management components manually
"""

import subprocess
import sys
import time
import threading
import os

def run_command(command, name, cwd=None):
    """Run a command in a subprocess and print its output"""
    try:
        print(f"Starting {name}...")
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=cwd
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
    print("Starting 5G Core Management Components...")
    print("This will start all management components: NETCONF Server, RESTCONF Server, SNMP Agent, and Web Dashboard")
    print("Note: Open5GS Docker containers are not started due to configuration issues")
    print("Press Ctrl+C to stop all services")
    
    # Start NETCONF server (which includes RESTCONF)
    print("\n1. Starting NETCONF/RESTCONF Server...")
    netconf_path = os.path.join("5g-core-management", "management-plane", "netconf-server", "netconf_server.py")
    netconf_thread = threading.Thread(
        target=run_command,
        args=(f"{sys.executable} {netconf_path}", "NETCONF/RESTCONF Server")
    )
    netconf_thread.daemon = True
    netconf_thread.start()
    
    # Note: RESTCONF is included in netconf_server.py, so we don't need a separate thread
    print("\n2. RESTCONF Server is included in NETCONF Server")
    
    # Start SNMP agent
    print("\n3. Starting SNMP Agent...")
    snmp_path = os.path.join("5g-core-management", "management-plane", "snmp-monitor", "snmp_agent.py")
    try:
        snmp_thread = threading.Thread(
            target=run_command,
            args=(f"{sys.executable} {snmp_path}", "SNMP Agent")
        )
        snmp_thread.daemon = True
        snmp_thread.start()
    except Exception as e:
        print(f"   Warning: Could not start SNMP Agent: {e}")
    # snmp_thread = threading.Thread(
    #     target=run_command,
    #     args=("python snmp_agent.py", "SNMP Agent", "5g-core-management/management-plane/snmp-monitor")
    # )
    # snmp_thread.daemon = True
    # snmp_thread.start()
    
    # Start Web Dashboard (if Node.js is available)
    print("\n4. Starting Web Dashboard...")
    web_dashboard_path = os.path.join("web-dashboard")
    if os.path.exists(os.path.join(web_dashboard_path, "node_modules")):
        try:
            dashboard_thread = threading.Thread(
                target=run_command,
                args=("npm start", "Web Dashboard", web_dashboard_path)
            )
            dashboard_thread.daemon = True
            dashboard_thread.start()
        except Exception as e:
            print(f"   Warning: Could not start Web Dashboard: {e}")
            print("   (Node.js/npm may not be installed or in PATH)")
    else:
        print("   Skipping Web Dashboard (node_modules not found)")
        print("   Install Node.js and run 'npm install' in web-dashboard directory")
    
    print("\nAll management components started!")
    print("\nAccess the components at:")
    print("- NETCONF Server: Port 830")
    print("- RESTCONF API: http://localhost:830/restconf")
    print("- RESTCONF Endpoints:")
    print("  * http://localhost:830/restconf/data/network-functions")
    print("  * http://localhost:830/restconf/data/subscribers")
    print("  * http://localhost:830/restconf/data/sessions")
    print("  * http://localhost:830/restconf/data/qos-profiles")
    print("- SNMP Agent: localhost:161")
    print("- Web Dashboard: http://localhost:3000 (if started)")
    print("\nPress Ctrl+C to stop all services")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down all services...")
        print("All services stopped. Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()