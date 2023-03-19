#!/bin/python3

import serial
import time # Optional (required if using time.sleep() below)
import numpy as np
import pandas as pd
import sys

def read_density(filename='/home/user/Scaricati/density.csv'):
    
    import subprocess
    command = 'tail -1 '+filename+' && echo "" > '+filename
    status, output = subprocess.getstatusoutput(command)
    if status==0:
        dtmp = output.split(',')
        data = "{:.2f} {:.2f}".format(float(dtmp[2])-273.15, float(dtmp[3]))
    else:
        data = "-1 -1"
    return data

def get_xml_url(url = "http://localhost:8082/values.xml"):
    import requests
    import xmltodict

    response = requests.get(url)
    return xmltodict.parse(response.content)

def append_srt2file(file, data):
    try:
        hs = open(file,"a")
        hs.write(data+"\n")
        hs.close() 
    except:
        print("ERROR writing file")
        sys.exit(3)
    return

def dump_Tsensor(url = "192.168.1.126", verbose=False):
    import time
    
    # colums=['T_room [C]', 'H_room [%]', 'D_room [C]', 'P_room [hP]']

    urladd = "http://"+url+"/values.xml"  
    try:
        data = get_xml_url(urladd)

        value = "{} {} {} {}".format(
                        data['root']['ch1']['aval'], 
                        data['root']['ch2']['aval'], 
                        data['root']['ch3']['aval'], 
                        data['root']['ch4']['aval'])
    except:
        print("ERROR reading Tsensor device")
        value = "-1 -1 -1 -1"
    return value

def append2sql(table_name, colums, df, verbose):
    import cygno as cy
    connection = cy.daq_sql_cennection(verbose=False)
    if connection:
        cy.cmd.push_panda_table_sql(connection=connection, table_name=table_name, df=df)
    else:
        sys.exit(2)
def main(update, file, sql, url, verbose):

    try:
        ser0 = serial.Serial(port='/dev/ttyACM0', baudrate=9600)

        ser1 = serial.Serial(port='/dev/ttyACM1', baudrate=9600)

        ser2 = serial.Serial(port='/dev/ttyS0', baudrate=9600)
    except:
        print("ERROR init serials device")   
        sys.exit(1)

    d0 = ['-1', '-1', '-1']
    d1 = ['-1', '-1', '-1']
    d2 = '-1'
    
    sql_columns=['timestamp', 'P_in', 'H_in', 'T_in',  'P_out', 'H_out', 
             'T_out', 'T_room', 'H_room', 'D_room', 'P_room', 'CF4', 'T_density', 'density']

    table_name = "slow_lab_test"
    start=time.time()
    syncwait = False
    try:
        while (True):
            try:
                if (ser2.inWaiting() > 0):
                    # read the bytes and convert from binary array to ASCII
                    data_str2 = ser2.read(ser2.inWaiting()).decode('ascii') 
                    if "ST" in data_str2:
                        d2 = data_str2.split(",")[1].split(" ")[1]
            except:
                print("ERROR reading flux meter % device")
                d2 = '-1'

            try:
                if (ser0.inWaiting() > 0):
                    # read the bytes and convert from binary array to ASCII
                    data_str0 = ser0.read(ser0.inWaiting()).decode('ascii') 
                    d0 = data_str0.split(" ")[0:3]
                    syncwait = True
            except:
                print("ERROR reading flux meter % device")
                d0 = ['-1', '-1', '-1']   

            end = time.time()

            try:
                if (ser1.inWaiting() > 0 and syncwait):
                    data_str1 = ser1.read(ser1.inWaiting()).decode('ascii')
                    d1 = data_str1.split(" ")[0:3] 
            except:
                print("ERROR reading flux meter % device")
                d1 = ['-1', '-1', '-1']        

            if len(d0)==3 and len(d1)==3 and end-start>update:
                d4 = read_density()
                data = str(int(end))+" "+datetime.datetime.utcfromtimestamp(int(end)).strftime('%Y-%m-%d %H:%M:%S')+\
                      " "+' '.join(d0)+" "+' '.join(d1)+" "+dump_Tsensor(url, verbose)+" "+d2+" "+d4
                if verbose: print(data) 
                append_srt2file(file, data)
                if sql:
                    data = data.split(' ')
                    del data[1:3]
                    df = pd.DataFrame(np.reshape(data, (1,len(data))),columns=sql_columns)
                    append2sql(table_name, sql_columns, df, verbose)
                start=time.time()
            time.sleep(0.1) 
            
    except KeyboardInterrupt:
        print('Bye!')
        sys.exit(0)

if __name__ == '__main__':
    from optparse import OptionParser
    import datetime

    now = datetime.datetime.now()
    fout = "data_sensors_"+now.strftime("%Y%m%d_%H%M")+".log"

    parser = OptionParser(usage='Tsenosr.py ')
    parser.add_option('-u','--url', dest='url', type='string', default='192.168.1.126', help='sensor ip address;');
    parser.add_option('-f','--file', dest='file', type="string", default=fout, help='output file;');
    parser.add_option('-t','--uptime', dest='uptime', type='string', default='600', help='file uptime;');
    parser.add_option('-s','--sql', dest='sql', action="store_true", default=False, help='dump on sql;');
    parser.add_option('-v','--verbose', dest='verbose', action="store_true", default=False, help='verbose print;');
    (options, args) = parser.parse_args()
    print (" T/P sensor at ip: {}\n log started on file: {}\n updated avery {} seconds".format(options.url, options.file, options.uptime))
    if options.file == fout:
        txt_columns='unix date hour P_in_[hP] H_in_[%] T_in_[C] P_out_[hP] H_out_[%] T_out_[C] T_room_[C] H_room_[%] D_room_[C] P_room_[hP] CF4'
        append_srt2file(options.file, txt_columns)
    main(update=int(options.uptime), file= options.file, sql = options.sql, url = options.url, verbose=options.verbose)
