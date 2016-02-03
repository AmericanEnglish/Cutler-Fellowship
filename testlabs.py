from Crypto.Hash import SHA256
from database import DB
from datetime import datetime
from matplotlib import pyplot
from numpy import polyfit
from numpy import poly1d
from numpy import array
from numpy import zeros
from os import listdir
from os.path import isdir
from os.path import isfile
from clean import *
from processing import *


def hash(phrase):
    """(str) -> bytes"""
    key = SHA256.new()
    key.update(phrase.encode(encoding='utf-8'))
    key = key.digest()
    return key


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
        p      | Plot. x_name,y_name. Also requires the -s flag
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
            print('+For relative pathing please use "./"')
            exit()
        if '/' == argv[index][-1]:
            print('+Remove trailing slash on -f argument')
            exit()
        # Check if it's a file
        if isfile(argv[index]):
            if ('dvt' not in item) and ('kplr' in item):
                into_db_timeseries(basebase, argv[index], item)
            elif ('dvt' in item) and ('kplr' in item):
                into_db_dvseries(basebase, argv[index], item)     
    else:
        print('WARNING: NO DATABASE FLAGS DETECTED')
    # Check for function flags
    if '-p' in argv:
        if '-s' in argv:
            index = argv.index('-p') + 1
            if ',' not in argv[index]:
                print('+Plot flag improperly formatted')
                exit()
            plot_items =  argv[index].split(',')
            index = argv.index('-s') + 1
            series_type = argv[index]
            if '-q' in argv:
                index = argv.index('-q') + 1
                quarter = argv[index]
            else:
                quarter = None
            pull_n_graph(basebase, plot_items[0], plot_items[1], series_type, quarter=quarter)

        else:
            print('ERROR: CANNOT PLOT BECAUSE NO -s FLAG DETECTED')
            exit()
    elif '-j' in argv:
        # This is where the stitching function is run
        for item in range(16):
            correct(basebase, 'cadenceno', 'sap_flux', 'time', str(item + 2))
        # stitching()
    elif '-s' in argv:
        print('ERROR: CANNOT PLOT WITHOUT A PROPER -p OR -j FLAG')
    else:
        print('WARNING: NO FUNCTION FLAGS DETECTED')

def correct(Database, x, y, series_type, quarter):
    ############### IMPROPER SQL STATEMENT
    query = """SELECT {0}, {1} 
        FROM {2}_data INNER JOIN {2}_defaults ON
            ({2}_data.filename = {2}_defaults.filename)
        WHERE {2}_defaults.name = 'QUARTER' 
            AND {2}_defaults.value = '{3}';""".format(x, y, series_type, quarter)
    print(query)
    Database.execute(query)
    ###############
    data = Database.fetchall()
    # print('Graphing')
    standin = []
    for item in data:
        if item[1] != None and item[0] != None:
            standin.append(item)
    data = standin
    x_dat, y_dat = zip(*data)
    x_dat = array(x_dat, dtype=float)
    y_dat = array(y_dat, dtype=float)
    new_y = get_fit(x_dat, y_dat, 2)
    # Set figure number
    pyplot.figure(quarter)
    pyplot.scatter(x_dat,y_dat, s=10, color='blue')
    pyplot.scatter(x_dat, new_y, s=10, color='red')
    pyplot.xlabel(x)
    pyplot.ylabel(y)
    pyplot.savefig("plot{}.png".format(datetime.now()).replace(' ', '-'))


if __name__ == '__main__':
    from sys import argv
    main(argv)