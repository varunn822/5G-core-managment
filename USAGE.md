# 5G Core Management Prototype - Usage Guide

This document provides instructions on how to use the 5G Core Management Prototype for hands-on learning.

## Prerequisites

Before starting, ensure you have the following installed:
- Docker and Docker Compose
- Python 3.8 or higher
- Node.js 14 or higher
- Git (optional, for version control)

## Installation

1. Clone or download this repository to your local machine
2. Navigate to the project directory
3. Install all dependencies by running:
   ```bash
   python install_dependencies.py
   ```
   Or manually install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r netconf/requirements.txt
   pip install -r restconf/requirements.txt
   pip install -r snmp/requirements.txt
   cd web-dashboard && npm install
   ```

## Starting the Prototype

### Option 1: Start All Components Together (Recommended)

Run the main script to start all components:
```bash
python run_all.py
```

This will start:
- Open5GS 5G core network functions
- NETCONF server on port 8080
- RESTCONF server on port 8081
- SNMP agent on port 161
- Web dashboard on port 3000

### Option 2: Start Components Individually

1. Start Open5GS:
   ```bash
   docker-compose up -d
   ```

2. Start NETCONF server:
   ```bash
   python netconf/netconf_server.py
   ```

3. Start RESTCONF server:
   ```bash
   python restconf/restconf_server.py
   ```

4. Start SNMP agent:
   ```bash
   python snmp/snmp_agent.py
   ```

5. Start Web Dashboard:
   ```bash
   cd web-dashboard
   npm start
   ```

## Accessing the Components

Once all components are running, you can access them at:

- **Web Dashboard**: http://localhost:3000
- **RESTCONF API**: http://localhost:8081/restconf
- **Open5GS Web UI**: http://localhost:3000
- **SNMP Agent**: localhost:161 (SNMP queries)

## Using the Management Interfaces

### RESTCONF API

The RESTCONF API provides a web-based interface for managing the 5G core network. You can:

1. Get all network functions:
   ```bash
   curl http://localhost:8081/restconf/data/network-functions
   ```

2. Get specific AMF:
   ```bash
   curl http://localhost:8081/restconf/data/network-functions/amf/amf-001
   ```

3. Create new AMF:
   ```bash
   curl -X POST http://localhost:8081/restconf/data/network-functions/amf \
        -H "Content-Type: application/json" \
        -d '{"id": "amf-002", "status": "active", "capacity": 30}'
   ```

### NETCONF Server

The NETCONF server provides configuration management using YANG models. You can connect to it using any NETCONF client.

### SNMP Agent

The SNMP agent exposes metrics from the 5G core network functions. You can query it using SNMP tools like `snmpwalk`:

```bash
snmpwalk -v2c -c public localhost:161 1.3.6.1.4.1.55555
```

## YANG Models

The prototype includes two YANG models:

1. **5G Core Network Functions** (`yang/5g-core-nf.yang`):
   - AMF management
   - SMF management
   - UPF management

2. **5G Subscriber Management** (`yang/5g-subscriber.yang`):
   - Subscriber provisioning
   - Security parameters
   - QoS settings

You can validate these models using pyang:
```bash
pyang -f tree yang/5g-core-nf.yang
pyang -f tree yang/5g-subscriber.yang
```

## Web Dashboard

The web dashboard provides a visual interface for monitoring the 5G core network:

1. Real-time metrics display
2. Network functions status
3. Subscriber information

The dashboard automatically updates every 5 seconds with the latest data from the network functions.

## Stopping the Prototype

To stop all components when running with the main script, simply press `Ctrl+C`.

When running components individually, stop each one separately:
```bash
docker-compose down  # Stop Open5GS
# Press Ctrl+C in each terminal running the other components
```

## Troubleshooting

### Common Issues

1. **Port conflicts**: If ports are already in use, modify the docker-compose.yml and server files to use different ports.

2. **Docker permission issues**: On Linux, you might need to run Docker commands with sudo or add your user to the docker group.

3. **Python dependencies**: If you encounter issues with Python dependencies, try creating a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Node.js issues**: Ensure you have Node.js 14 or higher installed for the web dashboard.

### Logs and Debugging

Each component outputs logs to the terminal. Check these logs for error messages and debugging information.

## Learning Exercises

### Exercise 1: Explore the YANG Models
1. Use pyang to generate a tree representation of the YANG models
2. Identify the key configuration parameters for each network function

### Exercise 2: Configure Network Functions via RESTCONF
1. Use curl or a REST client to retrieve current configurations
2. Modify a network function's configuration
3. Verify the changes were applied

### Exercise 3: Monitor Metrics via SNMP
1. Use snmpwalk to retrieve metrics from the SNMP agent
2. Observe how metrics change over time
3. Correlate metrics with network activity

### Exercise 4: Use the Web Dashboard
1. Observe real-time metrics in the dashboard
2. Identify patterns in network function utilization
3. Simulate network changes and observe the impact on metrics

## Next Steps

This prototype provides a foundation for learning 5G core network management. Consider extending it by:

1. Adding more network functions
2. Implementing more sophisticated YANG models
3. Adding authentication and authorization to the management interfaces
4. Integrating with real monitoring tools
5. Adding fault management capabilities

## Contributing

This is an educational prototype. Contributions are welcome to improve its functionality and educational value.