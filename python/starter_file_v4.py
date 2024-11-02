from pymodbus.client import ModbusSerialClient
import struct

# Serial configuration
PORT = '/dev/ttyUSB0'  # Change this to your actual serial port
BAUDRATE = 9600
SLAVE_ID = 1  # Change according to your device

# Create Modbus client
client = ModbusSerialClient(port=PORT, baudrate=BAUDRATE, timeout=1)

def write_pulse_per_revolution(value):
    """Writes the pulse per revolution to the motor driver."""
    high_register_value = 0x00  # High 16 bits set to 0
    low_register_value = value    # Actual value for low 16 bits

    # Write high register (address + 0)
    response_high = client.write_register(address=0x0001, value=high_register_value, slave=SLAVE_ID)
    
    if response_high.isError():
        print(f"Failed to write high register: {response_high}")
        return

    # Write low register (address + 1)
    response_low = client.write_register(address=0x0002, value=low_register_value, slave=SLAVE_ID)
    
    if response_low.isError():
        print(f"Failed to write low register: {response_low}")
        return

    print(f"Successfully set pulse/revolution to {value}")

if __name__ == "__main__":
    pulse_revolution_value = 10000  # Example value
    write_pulse_per_revolution(pulse_revolution_value)
