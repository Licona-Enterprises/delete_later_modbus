Modbbus debug steps attempt 1 Nov 3 2024 
---

# Modbus RS485 Stepper Motor Setup and Debugging Guide

This guide covers setting up and debugging the Modbus RS485 connection to your stepper motor driver (Model: Modbus RS485 Stepper Driver, 0.1-5.6A 24-48VDC for Nema 17, 23, 24 Stepper Motors) on a Raspberry Pi using `/dev/ttyUSB0`.

## Requirements

- Raspberry Pi with a USB-to-RS485 adapter
- Modbus RS485 Stepper Driver (compatible with Nema 17, 23, or 24 stepper motors)
- Python 3 and `pymodbus` library (if using the Python method)
- `modpoll` tool (if using the command-line method)

---

## Step 1: Configure Serial Port Settings on the Raspberry Pi

1. **Identify the Serial Port**  
   Connect your USB-to-RS485 adapter, and ensure it’s recognized as `/dev/ttyUSB0`. If not, adjust commands below for the correct port.

2. **Check Serial Port Settings**  
   Use `stty` to view the current settings of `/dev/ttyUSB0`:

   ```bash
   stty -F /dev/ttyUSB0 -a
   ```

   Look for:
   - **Baud rate**: e.g., 9600, 19200, or 115200 (based on driver specifications)
   - **Data bits**: Typically 8
   - **Parity**: Usually none for Modbus
   - **Stop bits**: Often 1, sometimes 2

3. **Set Serial Port Parameters**  
   Configure the port with the following (adjust based on driver requirements):

   ```bash
   sudo stty -F /dev/ttyUSB0 9600 cs8 -cstopb -parenb
   ```

   Replace `9600` with the appropriate baud rate if it differs.

---

## Step 2: Confirm Modbus Settings on the Stepper Driver

Check the stepper driver’s documentation for required settings:
- **Baud rate**
- **Data bits**
- **Parity**
- **Stop bits**
- **Modbus Slave ID** (address for the device)

These settings need to match your Raspberry Pi’s serial configuration.

---

## Step 3: Test Communication with a Modbus Tool

### Option A: Using `modpoll`

`modpoll` is a command-line tool for Modbus. Install `modpoll` if you haven’t already, and use it to test the connection:

1. **Install `modpoll`**  
   Download and install `modpoll` from [https://www.modbusdriver.com/modpoll.html](https://www.modbusdriver.com/modpoll.html).

2. **Run `modpoll` Command**  

   ```bash
   sudo modpoll -m rtu -a [slave_id] -r [register_address] -b [baud_rate] -p none -s 1 -d 8 /dev/ttyUSB0
   ```

   Replace:
   - `[slave_id]`: Modbus address of the driver
   - `[register_address]`: Valid register address from the driver’s documentation
   - `[baud_rate]`: Baud rate of the driver

   If settings are correct, you should see a response from the motor driver.

---

### Option B: Using Python with `pymodbus`

Alternatively, you can use a Python script to test the Modbus connection.

1. **Install `pymodbus`**  
   Install the library with:

   ```bash
   pip install pymodbus
   ```

2. **Run the Python Script**  

   ```python
   from pymodbus.client.sync import ModbusSerialClient

   client = ModbusSerialClient(
       method='rtu',
       port='/dev/ttyUSB0',
       baudrate=9600,    # Set to match motor settings
       parity='N',       # Adjust parity if required
       stopbits=1,       # Adjust if using 2 stop bits
       bytesize=8,
       timeout=1
   )

   client.connect()

   # Modify address/count as per driver’s register map
   response = client.read_holding_registers(address=0x0000, count=2, unit=1)  
   if response.isError():
       print("Error reading from device")
   else:
       print(response.registers)

   client.close()
   ```

   Replace `baudrate`, `parity`, `stopbits`, and `unit` (Modbus slave ID) with the actual values for your driver.

   - **Success**: You should see register values printed out.
   - **Error**: An error indicates a mismatch in settings or communication issues.

---

## Troubleshooting

- **No Response / Timeouts**: Double-check all serial and Modbus settings. Ensure the slave ID, baud rate, parity, stop bits, and data bits match between the Raspberry Pi and the driver.
- **Permission Errors**: Add your user to the `dialout` group (Linux) to avoid using `sudo`:

   ```bash
   sudo usermod -aG dialout $(whoami)
   ```

- **Physical Connection Issues**: Ensure all RS485 connections (A+, B-) are secure and correctly wired to the driver.

---

This should provide a handy reference for debugging and setting up the Modbus RS485 stepper motor connection on your Raspberry Pi. Happy debugging!