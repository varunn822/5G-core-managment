#!/usr/bin/env python3
"""
Quick test script to verify RESTCONF server is running
"""

import sys
import socket
import urllib.request
import json

def test_port(host, port):
    """Test if a port is open"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"Error testing port: {e}")
        return False

def test_restconf_endpoint(url):
    """Test RESTCONF endpoint"""
    try:
        req = urllib.request.Request(url)
        req.add_header('Accept', 'application/json')
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode())
            return True, response.status, data
    except urllib.error.HTTPError as e:
        return False, e.code, None
    except Exception as e:
        return False, None, str(e)

if __name__ == "__main__":
    print("Testing 5G Core Management Server...")
    print("=" * 50)
    
    # Test port 830
    print("\n1. Testing port 830...")
    if test_port('localhost', 830):
        print("   ✓ Port 830 is OPEN")
    else:
        print("   ✗ Port 830 is CLOSED or not accessible")
        print("   Please start the server first:")
        print("   python 5g-core-management/management-plane/netconf-server/netconf_server.py")
        sys.exit(1)
    
    # Test RESTCONF endpoint
    print("\n2. Testing RESTCONF API...")
    endpoints = [
        "http://localhost:830/restconf/data/network-functions",
        "http://localhost:830/restconf/data/subscribers",
        "http://localhost:830/restconf/data/sessions",
        "http://localhost:830/restconf/data/qos-profiles"
    ]
    
    for endpoint in endpoints:
        success, status, data = test_restconf_endpoint(endpoint)
        if success:
            print(f"   ✓ {endpoint}")
            print(f"     Status: {status}")
            if data:
                print(f"     Response keys: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
        else:
            print(f"   ✗ {endpoint}")
            print(f"     Error: {status or data}")
    
    print("\n" + "=" * 50)
    print("Test completed!")

