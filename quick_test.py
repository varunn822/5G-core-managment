#!/usr/bin/env python3
"""Quick test of RESTCONF API"""

import urllib.request
import json
import sys

try:
    print("Testing RESTCONF API...")
    print("-" * 50)
    
    # Test network-functions endpoint
    url = "http://localhost:830/restconf/data/network-functions"
    req = urllib.request.Request(url)
    req.add_header('Accept', 'application/json')
    
    with urllib.request.urlopen(req, timeout=3) as response:
        data = json.loads(response.read().decode())
        print(f"✓ SUCCESS! Server is running on port 830")
        print(f"✓ Status Code: {response.status}")
        print(f"\nResponse Data:")
        print(json.dumps(data, indent=2))
        
except urllib.error.URLError as e:
    print(f"✗ ERROR: Cannot connect to server")
    print(f"  {e}")
    print("\nMake sure the server is running:")
    print("  python setup_and_run.py")
    sys.exit(1)
except Exception as e:
    print(f"✗ ERROR: {e}")
    sys.exit(1)

