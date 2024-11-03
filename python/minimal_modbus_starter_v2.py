import serial
import minimalmodbus
from time import sleep

PORT = '/dev/ttyUSB0'
BAUDRATE = 9600
SLAVE_ID = 1  

client1 = minimalmodbus.Instrument(port=PORT, slaveaddress=SLAVE_ID, debug=True)
client1.serial.baudrate = 115200  # baudrate
client1.serial.bytesize = 8
client1.serial.parity   = serial.PARITY_EVEN
client1.serial.stopbits = 1
client1.serial.timeout  = 0.1      # seconds
client1.address         = 1        # this is the slave address number
client1.mode = minimalmodbus.MODE_RTU # rtu or ascii mode
client1.clear_buffers_before_each_transaction = True

client1.write_register(int("0x007D", 0), int("0x0000", 0), functioncode=6) # Stop

input_stats  = client1.read_register(125) # read single register 2bytes (16bit)
print("input stats: {0:016b}".format(input_stats))
output_stats  = client1.read_register(127) # read single register 2bytes (16bit)
print("output stats: {0:016b}".format(output_stats))