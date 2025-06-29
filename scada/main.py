from pymodbus.client import ModbusTcpClient
import time

client = ModbusTcpClient("plc_m340", port=502)
client.connect()

try:
    while True:
        rr = client.read_holding_registers(0, 3, unit=1)
        if rr.isError():
            print("Read error:", rr)
        else:
            print("PLC values:", rr.registers)
        time.sleep(2)
except KeyboardInterrupt:
    pass
finally:
    client.close()
