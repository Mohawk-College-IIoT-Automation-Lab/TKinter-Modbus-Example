from pymodbus.client import ModbusTcpClient
import time

DEFAULT_ADDR = "192.168.1.177"
DEFAULT_PORT = 502

COLOR_FORMAT_STRING = "#%02x%02x%02x"
MAC_FORMAT_STRING = "#%02x:%02x:%02x:%02x:%02x"
IP_FORMAT_STRING = "%d,%d,%d,%d"

CONNECT_COLOR = COLOR_FORMAT_STRING % (0, 255, 0)
DISCONNECT_COLOR = COLOR_FORMAT_STRING % (255, 0, 0)

ON_COLOUR = COLOR_FORMAT_STRING % (56, 177, 224)
OFF_COLOUR = COLOR_FORMAT_STRING % (87, 32, 32)

# REGISTER MAP

EN_COIL_ADDR = 10001
BRIGHTNESS_INPUT_ADDR = 20001

RED_CHAN_INPUT_ADDR = 20002
GREEN_CHAN_INPUT_ADDR = 20003
BLUE_CHAN_INPUT_ADDR = 20004
BRIGHTNESS_INPUT_ADDR = 20005

UID_HOLDING_REG = 40001
MAC_HOLDING_REG = 40002


client = ModbusTcpClient(host=DEFAULT_ADDR, port=DEFAULT_PORT)

if client.connect():
    if client.connected:
        pdu = client.write_register(address= UID_HOLDING_REG, value= 1, slave= 1)
        print(pdu)

        pdu = client.read_holding_registers(address= UID_HOLDING_REG, count= 1, slave= 1)
        print(pdu)

        time.sleep(2)

        pdu = client.read_holding_registers(address= UID_HOLDING_REG, count= 1, slave= 1)
        print(pdu)

client.close()