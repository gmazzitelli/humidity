#!/bin/python3

import minimalmodbus

PORT='/dev/ttyUSB0'
TEMP_REGISTER = 40100
HUM_REGISTER = 102

#Set up instrument
instrument = minimalmodbus.Instrument(PORT,1,mode=minimalmodbus.MODE_RTU)

#Make the settings explicit
instrument.serial.baudrate = 9600        # Baud
instrument.serial.bytesize = 8
instrument.serial.parity   = minimalmodbus.serial.PARITY_EVEN
instrument.serial.stopbits = 1
instrument.serial.timeout  = 1          # seconds

# Good practice
instrument.close_port_after_each_call = True

instrument.clear_buffers_before_each_transaction = True

# Read temperatureas a float
# if you need to read a 16 bit register use instrument.read_register()
temperature = instrument.read_float(TEMP_REGISTER)
#temperature = instrument.read_register(TEMP_REGISTER)

# Read the humidity
#humidity = instrument.read_float(HUM_REGISTER)

#Pront the values
print('The temperature is: %.1f deg C\r' % temperature)
#print('The humidity is: %.1f percent\r' % humidity)