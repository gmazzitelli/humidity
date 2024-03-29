#!/bin/python3
def append2sql(table_name, colums, df, verbose):
    import cygno as cy
    connection = cy.daq_sql_cennection(verbose=False)
    if connection:
        cy.cmd.push_panda_table_sql(connection=connection, table_name=table_name, df=df)
    else:
        sys.exit(2)

def read_density(filename='/home/user/Scaricati/density.csv'):

    import subprocess
    command = 'tail -1 '+filename+' && echo "" > '+filename
    status, output = subprocess.getstatusoutput(command)
    dtmp = output.split(';')
    d4 = "{:.2f} {:.2f}".format(float(dtmp[2].replace(',','.'))-273.15, float(dtmp[4].replace(',','.')))
    return d4

def main(file, verbose):
    import time
    import datetime
    import pandas as pd
    import numpy as np
    sql_columns=['time', 'T_density', 'density']
    table_name = "density"

    density = read_density(file)

    if verbose: print (density)
    data = str(int(time.time()))+" "+density

    if verbose: print(data)
    data = data.split(' ')
    df = pd.DataFrame(np.reshape(data, (1,len(data))),columns=sql_columns)
    if verbose: print(df)
    append2sql(table_name, sql_columns, df, verbose)

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage='usage: %prog\t ')
#    parser.add_option('-t','--tag', dest='tag', type='string', default='LNGS', help='tag LNF/LNGS [LNGS];');
#    parser.add_option('-s','--session', dest='session', type='string', default='sentinel-wlcg', help='session [sentinel-wlcg];');
    parser.add_option('-v','--verbose', dest='verbose', action="store_true", default=False, help='verbose output;');
    (options, args) = parser.parse_args()
    if args[0]:
    	#print("file: "+args[0])
    	main(file=args[0], verbose=options.verbose)
    else:
        print("filename")
