#!/bin/python3

def read_density(filename='/home/user/Scaricati/density.csv'):
    
    import subprocess
    command = 'tail -1 '+filename+' && echo "" > '+filename
    status, output = subprocess.getstatusoutput(command)
    dtmp = output.split(',')
    d4 = "{:.2f} {:.2f}".format(float(dtmp[2])-273.15, float(dtmp[3]))
    return d4


print (read_density())