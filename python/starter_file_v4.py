from pymodbus.client import ModbusSerialClient
import logging

# Enable logging for debugging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Modbus connection parameters
PORT = '/dev/ttyUSB0'  # Replace with your actual port
BAUDRATE = 9600
SLAVE_ID = 1  # Adjust according to your device settings

# Create a Modbus client instance
client = ModbusSerialClient(port=PORT, baudrate=BAUDRATE, timeout=2)

def connect_modbus():
    """Establish connection to the Modbus client."""
    if not client.connect():
        print("Failed to connect to Modbus server")
        return False
    return True

def write_full_16bit_value(address, value):
    """Writes a full 16-bit integer value to the specified register address."""
    # Ensure the value is within the 16-bit range
    if not (0 <= value <= 0xFFFF):
        raise ValueError("Value must be a 16-bit unsigned integer (0-65535)")

    # Write to the register
    response = client.write_register(address=address, value=value, slave=SLAVE_ID)
    
    if response.isError():
        print(f"Failed to write register at address {address}: {response}")
    else:
        print(f"Successfully wrote {value} to register at address {address}")

if __name__ == "__main__":
    if connect_modbus():
        register_address = 0x0001  # Register address to write to
        value_to_write = 200  # Normal human number to write as 16-bit
        write_full_16bit_value(register_address, value_to_write)

        # Close the connection
        client.close()
