#!/usr/bin/env python3
"""
Python-based web dashboard server for 5G Core Management
Serves the dashboard and connects to RESTCONF API
"""

from flask import Flask, send_from_directory, jsonify
import urllib.request
import json
import threading
import time
import os

app = Flask(__name__, static_folder='web-dashboard/public', static_url_path='')

# RESTCONF API base URL
RESTCONF_BASE = "http://localhost:830/restconf/data"

def fetch_restconf_data(endpoint):
    """Fetch data from RESTCONF API"""
    try:
        url = f"{RESTCONF_BASE}/{endpoint}"
        req = urllib.request.Request(url)
        req.add_header('Accept', 'application/json')
        with urllib.request.urlopen(req, timeout=2) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching {endpoint}: {e}")
        return {}

@app.route('/')
def index():
    """Serve the main dashboard page"""
    return send_from_directory('web-dashboard/public', 'index.html')

@app.route('/api/network-functions')
def get_network_functions():
    """Get network functions from RESTCONF API"""
    data = fetch_restconf_data('network-functions')
    return jsonify(data)

@app.route('/api/subscribers')
def get_subscribers():
    """Get subscribers from RESTCONF API"""
    data = fetch_restconf_data('subscribers')
    return jsonify(data)

@app.route('/api/sessions')
def get_sessions():
    """Get sessions from RESTCONF API"""
    data = fetch_restconf_data('sessions')
    return jsonify(data)

@app.route('/api/qos-profiles')
def get_qos_profiles():
    """Get QoS profiles from RESTCONF API"""
    data = fetch_restconf_data('qos-profiles')
    return jsonify(data)

@app.route('/api/metrics')
def get_metrics():
    """Generate metrics data (simulated)"""
    # Simulate metrics based on network functions
    try:
        nf_data = fetch_restconf_data('network-functions')
        amf_count = len(nf_data.get('amf', []))
        smf_count = len(nf_data.get('smf', []))
        upf_count = len(nf_data.get('upf', []))
        
        metrics = {
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S'),
            "amf": {
                "activeSessions": amf_count * 500 + 1000,
                "cpuUtilization": 30 + (amf_count * 5),
                "memoryUtilization": 50 + (amf_count * 3)
            },
            "smf": {
                "activePduSessions": smf_count * 400 + 900,
                "cpuUtilization": 25 + (smf_count * 5),
                "memoryUtilization": 45 + (smf_count * 3)
            },
            "upf": {
                "activeUsers": upf_count * 400 + 800,
                "throughput": upf_count * 50000000 + 100000000,
                "packetLoss": round(0.01 + (upf_count * 0.01), 2)
            }
        }
        return jsonify(metrics)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("5G Core Management - Web Dashboard Server")
    print("=" * 60)
    print(f"Dashboard: http://localhost:3000")
    print(f"RESTCONF API: {RESTCONF_BASE}")
    print("=" * 60)
    print("Press Ctrl+C to stop")
    print()
    
    app.run(host='0.0.0.0', port=3000, debug=False)

