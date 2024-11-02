from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time
# Configuration for RS485 connection
PORT = '/dev/ttyUSB0'  # Replace with your USB port
BAUDRATE = 9600        # Ensure this matches your motor driver configuration
TIMEOUT = 1
# Initialize the Modbus client
client = ModbusClient(
    method='rtu',
    port=PORT,
    baudrate=BAUDRATE,
    timeout=TIMEOUT,
    stopbits=1,
    bytesize=8,
    parity='N'
)
# Function to send command to run motor
def run_motor(driver_id, speed):
    # Example write to holding register (adjust address/register as per driver documentation)
    # Assuming speed control is handled via a holding register at address 0x0001
    speed_register_address = 0x0001
    response = client.write_register(speed_register_address, speed, unit=driver_id)
    if response.isError():
        print(f"Error sending command to motor {driver_id}")
    else:
        print(f"Motor {driver_id} set to speed {speed}")
# Function to stop motor
def stop_motor(driver_id):
    # Assuming stopping the motor is done by setting speed to 0
    stop_register_address = 0x0001
    response = client.write_register(stop_register_address, 0, unit=driver_id)
    if response.isError():
        print(f"Error stopping motor {driver_id}")
    else:
        print(f"Motor {driver_id} stopped")
# Connect to the RS485 network
if client.connect():
    print("Connected to RS485 network")
    # Run each motor at a specified speed for testing
    motor_speeds = [100, 150, 200, 250]  # Example speed values for each motor
    # Start each motor
    for i in range(4):
        driver_id = i + 1  # Assuming driver IDs are 1, 2, 3, and 4
        run_motor(driver_id, motor_speeds[i])
    # Run motors for 5 seconds
    time.sleep(5)
    # Stop each motor
    for i in range(4):
        driver_id = i + 1
        stop_motor(driver_id)
    # Disconnect from the RS485 network
    client.close()
    print("Disconnected from RS485 network")
else:
    print("Failed to connect to RS485 network")









