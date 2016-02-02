from Crypto.Hash import SHA256
from database import DB
from datetime import datetime
from matplotlib import pyplot
from numpy import polyfit
from numpy import poly1d
from numpy import array
from numpy import zeros
from os import listdir
from os import isdir
from os import isfile
from clean import *


def graph(Database, x, y, series_type):
    Database.connect()
    Database.cur_gen()
    ############### THIS IS SUPER NOT OK
    query = """SELECT {0}, {1} 
            FROM {2}_data""".format(x, y, series_type)
    print(query)
    Database.execute(query)
    ###############
    data = Database.fetchall()
    print('Graphing')
    x_dat, y_dat = zip(*data)
    pyplot.scatter(x_dat,y_dat, s=10)
    pyplot.xlabel(x)
    pyplot.ylabel(y)
    pyplot.savefig("plot{}.png".format(datetime.now()).replace(' ', '-'))


def hash(phrase):
    """(str) -> bytes"""
    key = SHA256.new()
    key.update(phrase.encode(encoding='utf-8'))
    key = key.digest()
    return key


def get_fit(x, y, deg):
    """(list, list, int) -> array(y coordinates)

    Takes the x coordinates and y coordinates of the series data and the degree
    of polynomial to be used for the best fit function. Then returns the 
    calculated points in an array. These are the new corected y values."""
    polynomial = polyfit(x, y, deg, rcond=None, full=False, w=None, cov=False)
    evalulate = poly1d(polynomial)
    new_data = zeros((1,len(x)))
    
    index = 0
    for item in x:
        new_data[index] = evalulate(item)

    return new_data


def main(argv):
    """(list of strs) -> None


    Only takes the sys.argv list. Uses this for parsing command line commands.
    Adding files to the database happens FIRST.
    $ python3 testlabs.py -FLAG ARGUMENT -FLAG ARGUMENT
    All flags       Purpose
        a      | Autodetect. Scans for unadded files and adds them automatically.
        c      | Smoothing. Plot x_name, smoothed_y. Only works from Times series.
        d      | Directory. This indicates you want to import a directory into the
        database instead of just one file
        f      | File. Put one specific file into the database
        p      | Plot. x_name, y_name. Also requires the -s flag
        s      | Series. Used for correct select series data. Time or DV.


    """
    basebase = DB('postgres', 'cutler', host='localhost', user='student', password='student')
    basebase.connect()
    basebase.cur_gen()
    # Check for DB add flags
    if '-a' in argv:
        pass
    elif '-d' in argv:
        index = argv.index('-d') + 1
        # Check if it's a directory
        if isdir(argv[index]):
            # Needs a trailing /
            if argv[index][-1] != '/':
                # Create one
                argv[index] = argv[index] + '/'
                print('+Be sure directories have a trailing /')
            # Loop through items in directory
            for item in listdir(argv[index]):
                if ('dvt' not in item) and (isfile(argv[index] + item)) and ('kplr' in item):
                    into_db_timeseries(basebase, argv[index], item)
                elif ('dvt' in item) and (isfile(argv[index] + item)) and ('kplr' in item):
                    into_db_dvseries(basebase, argv[index], item)
        else:
            print('ERROR: NOT A DIRECTORY')

    elif '-f' in argv:
        index = argv.index('-f') + 1
        # only absolute pathing only
        if '/' not in argv[index]:
            print('For relative pathing please use "./"')
            exit()
        if '/' == argv[index][-1]:
            print('Remove trailing slash on -f argument')
            exit()
        # Check if it's a file
        if isfile(argv[index]):
            if ('dvt' not in item) and ('kplr' in item):
                into_db_timeseries(basebase, argv[index], item)
            elif ('dvt' in item) and ('kplr' in item):
                into_db_dvseries(basebase, argv[index], item)     
    else:
        print('ERROR: NO DATABASE FLAGS DETECTED')
    # Check for function flags
    if '-p' in argv:
        if '-s' in argv:
            pass
        else:
            print('ERROR: CANNOT PLOT NO -s FLAG DETECTED')
            exit()
    elif '-s' in argv:
        print('ERROR: CANNOT PLOT WITHOUT A PROPER -p FLAG')
    else:
        print('ERROR: NO FUNCTION FLAGS DETECTED')


if __name__ == '__main__':
    from sys import argv
    main(argv)