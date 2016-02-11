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
import random
import warnings


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
        j      | Join. Stitches all quarters together into one VERY colorful graph
        p      | Plot. x_name,y_name. Also requires the -s flag
        s      | Series. Used for correct select series data. Time or DV.
        sbf    | show_best_fit. Calls this function. That's it.
        x      | Segmentation. Does segment based things. This should be a leading flag.
        o      | Dump. Dumps data from the database into a csv.

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
    if '-x' in argv:
        # Segmentation flags
        if '-q' in argv:
            quarter = argv[argv.index('-q') + 1]
        else:
            quarter = None
        if '-o' in argv:
            columns = argv[argv.index('-o') + 1].split(',')
            rip_to_local(basebase, columns, quarter)
            # ColumnNames
        elif '-sbf' in argv:
            seg_best_fit(basebase, argv[argv.index('-sbf') + 1].split(','), quarter)

        else:
            print('ERROR: NO SEGMENTATION ACTIONS DETECTED')
    elif '-p' in argv:
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
    elif '-sbf' in argv:
        if '-q' in argv:
            show_best_fit(basebase, 'cadenceno', 'sap_flux', 'time', argv.index('-q'))
        # This is where the show_best_fit function is run
        else:
            for item in range(17):
                show_best_fit(basebase, 'cadenceno', 'sap_flux', 'time', str(item + 1))
        # stitching()
    elif '-j' in argv:
        if '-s' in argv:
            x, y = argv[argv.index('-j') + 1].split(',')
            stitching(basebase, x, y, argv[argv.index('-s') + 1])
        else:
            print('ERROR: CANNOT PLOT BECAUSE NO -s FLAG DETECTED')
    elif '-s' in argv:
        print('ERROR: CANNOT PLOT WITHOUT A PROPER -p OR -j FLAG')
    else:
        print('WARNING: NO FUNCTION FLAGS DETECTED')

def seg_best_fit(basebase, columns, quarter):
    statement = """SELECT {}, {} FROM time_data
            INNER JOIN time_defaults ON (time_data.filename = time_defaults.filename)
            WHERE time_defaults.name = 'QUARTER' 
                AND time_defaults.value = '{}';"""
    if quarter == None:
        statement = statement.format(columns[0], columns[1], "{}")
    else:
        statement = statement.format(columns[0], column[1], quarter)

    total = 0
    for item in range(17):
        counter = 0
        item += 1
        query = statement.format(item)
        # print(query)
        basebase.execute(query)
        sub_data = basebase.fetchall()
        sub_data = segmentor(sub_data)
        for segment in sub_data:
            total += 1
            counter += 1
            print("Q{}:S{}:{}/{}".format(item, total, counter, len(sub_data)))
            x, y = zip(*segment)
            x, y = array(x, dtype=float), array(y, dtype=float)
            # Set figure number
            new_y = get_fit(x, y, 2)
            pyplot.scatter(x, y, s=10, color='blue')
            pyplot.scatter(x, new_y, s=10, color='red')
            pyplot.xlabel(columns[0])
            pyplot.ylabel(columns[1])
            pyplot.savefig("plot{}.seg_fit.S{}.Q{}.png".format(datetime.now(), total, item).replace(' ', '-'))
            pyplot.close()
            print(">>plot{}.seg_fit.S{}.Q{}.png".format(datetime.now(), total, item).replace(' ', '-'))



def segmentor(data):
    """List of tuples -> list of tuples

    Takes the data extracted from a database and segments the tuples using
    natural None serpators.

    [(num, num, num), (num, None, num), (num, num, num)]
    becomes
    [[(num, num, num)], [(num, num, num)]]"""
    index = 0
    new_data = []
    while index < len(data) - 1:# using the tracked list index
        standin = []
        while None in data[index]:
            index += 1
        for tup in data[index:]:
            if None not in tup:
                standin.append(tup)
                index += 1
            else:
                if len(standin) >= 15:
                    new_data.append(standin)
                break
    return new_data

if __name__ == '__main__':
    from sys import argv
    main(argv)