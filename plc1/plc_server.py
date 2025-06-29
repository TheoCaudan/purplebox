from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Starting script...")

try:
    store = ModbusSlaveContext(
        di = None,
        co = None,
        hr = None,
        ir = None
    )
    logging.info("Modbus slave context created")

    context = ModbusServerContext(slaves=store, single=True)
    logging.info("Modbus server context created")

    identity = ModbusDeviceIdentification()
    identity.VendorName = 'PurpleBox'
    identity.ProductCode = 'PB'
    identity.VendorUrl = 'https://example.com'
    identity.ProductName = 'SimPLC'
    identity.ModelName = 'v1'
    identity.MajorMinorRevision = '1.0'
    logging.info("Device identification set")

    logging.info("Starting Modbus TCP Server on 0.0.0.0:5020")
    StartTcpServer(context, identity=identity, address=("0.0.0.0", 5020))
    logging.error("Modbus TCP Server has stopped")

except Exception as e:
    logging.error(f"Exception occured: {e}")