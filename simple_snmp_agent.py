from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdrsp, context
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.carrier.asyncore.dispatch import AsyncoreDispatcher

# Create SNMP engine
snmpEngine = engine.SnmpEngine()

# Transport setup
config.addTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpTransport().openServerMode(('localhost', 161))
)

# SNMPv2c setup
config.addV1System(snmpEngine, 'test-agent', 'public')

config.addTargetParams(
    snmpEngine, 'test-params', 'test-agent', 'noAuthNoPriv', 1
)

# Create SNMP context
snmpContext = context.SnmpContext(snmpEngine)

# Register SNMP applications
cmdrsp.GetCommandResponder(snmpEngine, snmpContext)
cmdrsp.SetCommandResponder(snmpEngine, snmpContext)
cmdrsp.NextCommandResponder(snmpEngine, snmpContext)
cmdrsp.BulkCommandResponder(snmpEngine, snmpContext)

print("SNMP engine initialized")
print("Transport dispatcher:", snmpEngine.transportDispatcher)

# Run the dispatcher
try:
    snmpEngine.transportDispatcher.runDispatcher()
except KeyboardInterrupt:
    print("\nShutting down...")
    snmpEngine.transportDispatcher.closeDispatcher()