# Import necessary libraries for Modbus communication
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time

# Establish connection to the DM556RS using RS485
client = ModbusClient(
    method='rtu',                # Use RTU method for RS485
    port='/dev/ttyUSB0',         # Replace with the correct port for your RS485 adapter
    baudrate=115200,             # Baud rate, ensure this matches the DM556RS settings
    stopbits=1,
    bytesize=8,
    parity='N',
    timeout=1                    # Timeout in seconds
)

# Connect to the Modbus client
if client.connect():
    print("Connected to DM556RS Stepper Drive")
else:
    print("Failed to connect to DM556RS Stepper Drive")
    exit()

# Helper function to write to a single register
def write_register(register_address, value):
    response = client.write_register(register_address, value, unit=1)  # unit=1 for Slave ID 1
    if response.isError():
        print(f"Error writing to register {register_address}")
    else:
        print(f"Successfully wrote {value} to register {register_address}")

# Helper function to read from a register
def read_register(register_address, count=1):
    response = client.read_holding_registers(register_address, count, unit=1)
    if response.isError():
        print(f"Error reading from register {register_address}")
        return None
    else:
        print(f"Register {register_address} value: {response.registers}")
        return response.registers

# Step 1: Initial Configuration
# Enable the drive via RS485 (write 1 to register 0x00F)
write_register(0x00F, 1)  # Pr0.07 - Enable drive via RS485

# Set peak current (0x0191)
# Example: Set to 3.2A (0.1A units, so write 32)
write_register(0x0191, 32)

# Step 2: Control Setup
# JOG CW and CCW commands (0x1801 register)
# Example: Jog CW
write_register(0x1801, 0x4001)
print("Sent JOG CW command")

# Step 3: Testing and Tuning
# Read status to ensure proper operation
status = read_register(0x1003)  # Read motion state register
if status and status[0] & 0x02:  # Check if drive is enabled (Bit1)
    print("Drive is enabled and running")
else:
    print("Drive is not enabled or running")

# Close the client connection when done
client.close()
print("Connection closed")
