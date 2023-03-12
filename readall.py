#!/bin/python3

import serial
import time # Optional (required if using time.sleep() below)
import numpy as np
import pandas as pd

def get_xml_url(url = "http://localhost:8082/values.xml"):
    import requests
    import xmltodict

    response = requests.get(url)
    return xmltodict.parse(response.content)

def append_srt2file(file, data):
    hs = open(file,"a")
    hs.write(data+"\n")
    hs.close() 

def dump_Tsensor(url = "192.168.1.126", verbose=False):
    import time
    
    # colums=['T_room [C]', 'H_room [%]', 'D_room [C]', 'P_room [hP]']

    urladd = "http://"+url+"/values.xml"    
    data = get_xml_url(urladd)

    value = "{} {} {} {}".format(
                    data['root']['ch1']['aval'], 
                    data['root']['ch2']['aval'], 
                    data['root']['ch3']['aval'], 
                    data['root']['ch4']['aval'])
    return value

def append2sql(table_name, colums, df, verbose):
    import cygno as cy
    connection = cy.daq_sql_cennection(verbose=verbose)
    if connection:
        cy.cmd.push_panda_table_sql(connection=connection, table_name=table_name, df=df)

def main(update, file, sql, url, verbose):

    ser0 = serial.Serial(port='/dev/ttyACM0', baudrate=9600)

    ser1 = serial.Serial(port='/dev/ttyACM1', baudrate=9600)
    

    
    sql_columns=['timestamp', 'P_in', 'H_in', 'T_in',  'P_out', 'H_out', 
             'T_out', 'T_room', 'H_room', 'D_room', 'P_room']

    table_name = "slow_lab_test"
    start=time.time()
    syncwait = False
    while (True):

        if (ser0.inWaiting() > 0):
            # read the bytes and convert from binary array to ASCII
            data_str0 = ser0.read(ser0.inWaiting()).decode('ascii') 
            d0 = data_str0.split(" ")[0:3]

            syncwait = True
        end = time.time()
        if (ser1.inWaiting() > 0 and syncwait):

            data_str1 = ser1.read(ser1.inWaiting()).decode('ascii')
            d1 = data_str1.split(" ")[0:3] 
            if len(d0)==3 and len(d1)==3 and end-start>update:
                data = str(int(end))+" "+datetime.datetime.utcfromtimestamp(int(end)).strftime('%Y-%m-%d %H:%M:%S')+\
                      " "+' '.join(d0)+" "+' '.join(d1)+" "+dump_Tsensor(url, verbose)
                if verbose: print(data) 
                append_srt2file(file, data)
                if sql:
                    data = data.split(' ')
                    del data[1:3]
                    df = pd.DataFrame(np.reshape(data, (1,len(data))),columns=sql_columns)
                    append2sql(table_name, sql_columns, df, verbose)
                start=time.time()

        time.sleep(0.1) 


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
        txt_columns='unix date hour P_in_[hP] H_in_[%] T_in_[C] P_out_[hP] H_out_[%] T_out_[C] T_room_[C] H_room_[%] D_room_[C] P_room_[hP]'
        append_srt2file(options.file, txt_columns)
    main(update=int(options.uptime), file= options.file, sql = options.sql, url = options.url, verbose=options.verbose)
