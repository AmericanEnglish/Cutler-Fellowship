from Crypto.Hash import SHA256
from database import DB
from datetime import datetime
from matplotlib import pyplot
from numpy import polyfit
from numpy import poly1d
from numpy import array
from numpy import zeros
from os import listdir
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
        pass
    elif '-f' in argv:
        pass

    # Check for function flags
    if '':
        # success = basebase.create_table('generate_tables.sql')
        # if not success[0]:
        #     print(success[1])
        #     exit()
        for item in listdir(argv[1]):
            if 'kplr' in item:
                into_db_timeseries(basebase, argv[1], item)
    else:
        graph(basebase, argv[1], argv[2], argv[3])


if __name__ == '__main__':
    from sys import argv
    main(argv)