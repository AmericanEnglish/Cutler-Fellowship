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
        c      | Smoothing. Plot x_name, smoothed_y. Only works from Times series. -x sub flag requires -dat
        d      | Directory. This indicates you want to import a directory into the
        dat    | Data. Indicates the data to be used for some flags.
        database instead of just one file
        f      | File. Put one specific file into the database
        g      | Generate tables
        j      | Join. Stitches all quarters together into one VERY colorful graph
        p      | Plot. x_name,y_name. Also requires the -s flag
        s      | Series. Used for correct select series data. Time or DV.
        sbf    | show_best_fit. Calls this function. That's it.
        x      | Segmentation. Does segment based things. This should be a leading flag.
        o      | Dump. Dumps data from the database into a csv.
        t      | Trim. Uses a +/-5 percent band for data trimming & plotting
        zm     | Zoom. Zooms into a section of a graph. Uses '-r start,end' to function.

    """
    basebase = DB('postgres', 'cutler', host='localhost', user='student', password='student')
    basebase.connect()
    basebase.cur_gen()
    # Check for DB add flags
    if '-a' in argv:
        pass
    elif '-g' in argv:
        basebase.create_table('./generate_tables.sql')
        print('TABLES CREATED')
    elif '-drop' in argv:
        basebase.execute('DROP TABLE dv_data;')
        basebase.execute('DROP TABLE dv_defaults;')
        basebase.execute('DROP TABLE time_data;')
        basebase.execute('DROP TABLE time_defaults;')
        basebase.execute('DROP TABLE files;')
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
                if ('dvt' not in item) and (isfile(argv[index] + item)) and ('kplr' in item) and ('llc_lc.tbl' in item):
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
        elif '-c' in argv:
            index = argv.index('-c')
            if '-dat' not in argv:
                print('ERROR: DATA NOT SELECTED FOR SMOOTHING')
            elif len(argv[argv.index('-dat') + 1].split(',')) != 3:
                print('ERROR: INVALID NUMBER OF -dat ARGUMENTS\nPLEASE USE: 3')
                print(argv[argv.index('-dat') + 1].split(','))
            elif argv[index + 1] == 'sqr':
                # Square Smooth
                square_smooth(basebase, argv[argv.index('-dat') + 1].split(','))
            elif argv[index + 1] == 'tri':
                # Triangular Smooth
                triangular_smooth(basebase, argv[argv.index('-dat') + 1].split(','))
            elif argv[index + 1] == 'sav':
                # Savitzky-Golay Smooting
                pass
            elif argv[index + 1] == 'all':
                # Run all three
                square_smooth(basebase, argv[argv.index('-dat') + 1].split(','))
                triangular_smooth(basebase, argv[argv.index('-dat') + 1].split(','))

            else:
                print('ERROR: NO SMOOTHING TYPE DETECTED')
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
    elif '-zm' in argv:
        x, y = argv[argv.index('-zm') + 1].split(',')
        if '-r' in argv:
            start, end = argv[argv.index('-r') + 1].split(',')
            zoom(basebase, x, y, start, end)
        else:
            print('ERROR: NO -r FLAG DETECTED!')
    elif '-s' in argv:
        print('ERROR: CANNOT PLOT WITHOUT A PROPER -p OR -j FLAG')
    else:
        print('WARNING: NO FUNCTION FLAGS DETECTED')


def savitzky_golay_smooth():
    # Query database -> Maybe select the quarter so that it can be colored well
    # Segment data to remove bad data
    # Desegment
    # Smooth
    # Plot
    pass


def zoom(basebase, x, y, start, end):
    """(DB Object, string, string, num, num) -> None


    This allows the user to "zoom" into a segment of data. Simply by entering
    the xaxis and yaxis, the x start, and the x stop, the program will drop a
    a large blownup area of the requested section."""
    query = """SELECT {}, {} FROM time_data
            WHERE {} <= {} AND {} <= {};""".format(x, y, start, x, x, end)
    basebase.execute(query) # WHERE start < x AND x < end;
    data = basebase.fetchall()
    data.sort()
    if len(data) <= 1:
        query = """SELECT {}, {} FROM time_data
                WHERE {} <= {} AND {} <= {};""".format(x, y, start, x, x, end)
        print('Data is empty? Restructure your query:\n {}'.format(query))
        print(data)
        exit()
    x_dat, y_dat = zip(*data)
    pyplot.figure(figsize=(16,8), dpi=200) 
    pyplot.xlim(min(x_dat) - 1, max(x_dat) + 1)
    # pyplot.ylim(min(y_dat), max(y_dat))
    pyplot.plot(x_dat, y_dat, color='black')
    pyplot.xlabel(x)
    pyplot.ylabel(y)
    pyplot.suptitle("{0} vs {1} :: { {2} < {1} < {3}, {0}}".format(y, x, start, end))
    name = "zoomed_plot_{}.{}_{}.png".format(x,y, datetime.now())
    pyplot.savefig(name)
    print('>>{}'.format(name))


if __name__ == '__main__':
    from sys import argv
    main(argv)
