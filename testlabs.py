#!/usr/bin/env python3

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
        avg    | Averages. Plots segmental averages using a constant size.
        sum    | Drops segment calculated values. 
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
        t      | Trim. Uses a +/-5 percent band for data trimming & plotting

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
        if '-t' in argv:
            trim_segments(basebase)
        elif '-o' in argv:
            columns = argv[argv.index('-o') + 1].split(',')
            rip_to_local(basebase, columns, quarter)
            # ColumnNames
        elif '-sbf' in argv:
            seg_best_fit(basebase, argv[argv.index('-sbf') + 1].split(','), quarter)
        elif '-j' in argv:
            seg_stitch(basebase, argv[argv.index('-j') + 1].split(','), quarter)
        elif '-sum' in argv:
            generate_summary(basebase, argv[argv.index('-sum') + 1].split(','))
        elif '-avg' in argv:
            generate_segment_averages(basebase, argv[argv.index('-avg') + 1].split(','))
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

def trim_segments(basebase, columns):
    data = segmentor(data)
    trimmed = []
    for segment in data:
        trimmed.append(trim(segment, 5))


def trim(seg_data, percent):
    """(list of seg data) -> list of trimmed seg data

    Takes a list of pre segmented data and then returns a trimmed version of 
    that data using the percent. The operates under the assumptions that follow:

    1. Data will be fit with a line. 
    2. Data beyond the line five percent line will be trimmed
    3. The trimmed data will be returned [(num, num, num,), (num,num,num)]"""
    percent = 5/100.
    # Initial fit
    x, y = zip(*segment)
    new_y = get_fit(x, y, 2)
    trimmed_x = []
    trimmed_y = []
    for index, tup in enumerate(zip(y, new_y)):
        # This creates the artificial band
        if not ((tup[0] > (tup[1] + tup[1]*percent)) and (tup[0] < (tup[1] - tup[1]*percent))):
            trimmed_x.append(x[index])
            trimmed_y.append(tup[0])
        # Get a fit for the new data
        new_y = get_fit(trimmed_x, trimmed_y, 2)
        # Zip it back up
        new_segments.append(zip())


    # 5% trimming
    # New fit


if __name__ == '__main__':
    from sys import argv
    main(argv)