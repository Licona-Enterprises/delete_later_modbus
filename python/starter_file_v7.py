# Import necessary libraries for Modbus communication
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time

# Establish connection to the DM556RS using RS485
client = ModbusClient(
    #method='rtu',                # Use RTU method for RS485
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

'''
This section includes additional write register commands for stepper motor and wheels

# Step 1: Initial Configuration (enable drive)
write_register(0x00F, 1)  # Enable drive via RS485 (Pr0.07)

# Step 2: Control Setup - Configure Motion Parameters
# Set JOG velocity (register 0x01E1). Example: Set speed to 500 RPM (value depends on your driver specs)
write_register(0x01E1, 500)  # Adjust value as needed for desired speed

# Set acceleration (register 0x01E7). Example: Set acceleration to 200 RPM/s
write_register(0x01E7, 200)  # Adjust for acceleration/deceleration profile

# Step 3: Set the Control Command (e.g., start JOG CW)
write_register(0x1801, 0x4001)  # Start JOG CW (continuous clockwise rotation)

# Optional: Set deceleration (if separate deceleration register exists)
# write_register(0x01E8, 200)  # Example: Deceleration to match acceleration

# Step 4: Additional Motion Features
# If position control is required:
# Write to the target position register (e.g., 0x0201 for the position)
# write_register(0x0201, 1000)  # Move to a position (1000 steps/units, for example)

# Step 5: Verify motor status and ensure operation
status = read_register(0x1003)  # Read motion state register to check status
if status and status[0] & 0x02:  # Check if Bit1 indicates the drive is enabled and running
    print("Drive is enabled and motor is rotating")
else:
    print("Drive is not running as expected")
'''

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













