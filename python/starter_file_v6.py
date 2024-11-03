#!/usr/bin/env python3
import pymodbus
from pymodbus.client import ModbusSerialClient

PORT = '/dev/ttyUSB0' 
BAUDRATE = 115200       
SLAVE_ID = 1 

client = ModbusSerialClient(
    port=PORT,
    baudrate=BAUDRATE,
    stopbits=1,
    bytesize=8,
    parity='N',
    timeout=1
)

connection = client.connect()

read_vals  = client.read_holding_registers(248, 4, unit=1) # start_address, count, slave_id
print(read_vals.registers)

# write registers
write  = client.write_register(1,425,unit=1)# address = 1, value to set = 425, slave ID = 1