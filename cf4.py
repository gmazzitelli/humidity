#!/bin/python3
import serial
ser2 = serial.Serial(port='/dev/ttyS0', baudrate=9600)
while (True):
    if (ser2.inWaiting() > 0):
        # read the bytes and convert from binary array to ASCII
        data_str2 = ser2.read(ser2.inWaiting()).decode('ascii')
        if "ST" in data_str2:
            print(">>", data_str2.split(",")[1])

        