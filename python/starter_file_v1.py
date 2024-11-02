import time
from pymodbus.client import ModbusSerialClient

# Replace these with your specific configuration
PORT = '/dev/ttyUSB0'  # Change to your serial port
BAUDRATE = 9600         # Common baud rate for Modbus
SLAVE_ID = 1            # Slave ID for your Modbus device

# Create Modbus client
client = ModbusSerialClient(port=PORT, baudrate=BAUDRATE, timeout=1)

def send_motor_command(command):
    """Sends a command to the motor driver."""
    try:
        client.connect()
        # Sending a command to the motor (for example, setting speed or position)
        # Adjust the address and value according to your motor driver documentation
        response = client.write_register(0x01, command, slave=SLAVE_ID)  # Example address 0x01
        print(f"Response: {response}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client.close()

# Example usage: Move the motor to a position or set speed
if __name__ == "__main__":
    speed_command = 500  # Set the speed (value depends on your motor specification)
    send_motor_command(speed_command)
    time.sleep(1)  # Wait for a second

    # You can send more commands as needed
