from pymodbus.client import ModbusTcpClient
import time

time.sleep(15)

client = ModbusTcpClient("192.168.20.10", port=5020)
client.connect()

try:
    while True:
        rr = client.read_holding_registers(address=1, count=3)
        if rr.isError():
            print("Read error:", rr)
        else:
            print("PLC values:", rr.registers)
        time.sleep(2)
except KeyboardInterrupt:
    pass
finally:
    client.close()
