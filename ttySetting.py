#!/bin/python3

def main(dev):
    import serial

    SerialPortObj = serial.Serial(dev)

    print('\n-> ',SerialPortObj) 
    SerialPortObj.close()    

if __name__ == '__main__':
    from optparse import OptionParser
    import datetime
    import sys

    now = datetime.datetime.now()
    dev = "/dev/ttyS0"

    parser = OptionParser(usage='usage: %prog <dev> ['+dev+']')
    parser.add_option('-d','--dev', dest='dev', type='string', default=dev, help='dev');
    (options, args) = parser.parse_args()
    if len(sys.argv)==2:
        dev = args[0]
    main(dev)