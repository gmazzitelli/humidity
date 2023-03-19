#!/bin/python3

###########
import serial
import time
ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)
while (True):
    ser.write(b'\x01\x03\x00')
    val = ser.read()
    print(val)
    time.sleep(0.1)
#############
    
# from pymodbus.client.sync import ModbusSerialClient

# click = ModbusSerialClient(method='rtu',port='/dev/ttyUSB0',baudrate=9600,parity='0')
# click.connect()
# outputLight = click.read_coils(8193,1,unit=1)

# print outputLight