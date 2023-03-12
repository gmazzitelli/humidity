#!/bin/python3

import serial

SerialPortObj = serial.Serial('/dev/ttyUSB0')

print('\n-> ',SerialPortObj) 
SerialPortObj.close()    
