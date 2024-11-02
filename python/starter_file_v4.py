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

def write_32bit_value(address, low_value, high_value=0):
    """
    Writes a 32-bit integer value to two registers (high and low).
    high_value is the upper 16 bits, low_value is the lower 16 bits.
    """
    # Ensure the low_value and high_value are within the 16-bit range
    if not (0 <= low_value <= 0xFFFF):
        raise ValueError("Low value must be a 16-bit unsigned integer (0-65535)")
    if not (0 <= high_value <= 0xFFFF):
        raise ValueError("High value must be a 16-bit unsigned integer (0-65535)")

    # Write high register (address)
    response_high = client.write_register(address=address, value=high_value, slave=SLAVE_ID)
    
    if response_high.isError():
        print(f"Failed to write high register at address {address}: {response_high}")
        return

    # Write low register (address + 1)
    response_low = client.write_register(address=address + 1, value=low_value, slave=SLAVE_ID)
    
    if response_low.isError():
        print(f"Failed to write low register at address {address + 1}: {response_low}")
        return

    print(f"Successfully wrote high: {high_value}, low: {low_value} to registers starting at address {address}")

if __name__ == "__main__":
    if connect_modbus():
        register_address = 0x0001  # Starting register address
        low_value_to_write = 200  # Lower 16 bits to write
        high_value_to_write = 0  # Upper 16 bits (0 for 32-bit value 200)
        write_32bit_value(register_address, low_value_to_write, high_value_to_write)

        # Close the connection
        client.close()
