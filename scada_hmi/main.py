import time
import logging
from pymodbus.client import ModbusTcpClient

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

ip = "192.168.20.10"
port = 5020

time.sleep(5)

logging.info("Connecting to PLC...")
client = ModbusTcpClient(ip, port=port)

if client.connect():
    logging.info("Connected successfully")
else:
    logging.error("Failed to connect...")

try:
    while True:
        rr = client.read_holding_registers(address=0, count=3)
        if rr.isError():
            logging.error("Read error:", rr)
        else:
            logging.info("Register values:", rr.registers)
        time.sleep(5)

except KeyboardInterrupt:
    logging.info("Client stopped by user")

finally:
    client.close()
    logging.info("Connection closed")