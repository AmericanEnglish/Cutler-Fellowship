from numpy import RankWarning
from numpy import array
from numpy import polyfit
from numpy import zeros
from numpy import poly1d
from matplotlib import pyplot
from datetime import datetime
import warnings
import random


# For all the numerical processing & graphin functions
def avg(someset, rounded=True):
    if rounded:
        return round(sum(someset) / len(someset), 2)
    else:
        return sum(someset) / len(someset)


def generate_segment_averages(basebase, columns):
    statement = """SELECT {}, {} FROM time_data
            INNER JOIN time_defaults ON (time_data.filename = time_defaults.filename)
            WHERE time_defaults.name = 'QUARTER' 
                AND time_defaults.value = '{}';""".format(columns[0], columns[1], '{}')
    chunk_size = int(columns[-1])
    total = 0
    pyplot.figure(figsize=(16,8), dpi=200) 
    # r helps generate a random color in hex
    # r = lambda: random.randint(0,255)
    total = 0
    basebase.execute("""SELECT MIN({0}), MAX({0}) FROM time_data;""".format(columns[1]))
    ylimits = basebase.fetchall()[0]
    ylimits = (round(ylimits[0]), round(ylimits[1]))
    for item in range(17):
        # color=('#%02X%02X%02X' % (r(),r(),r()))
        counter = 0
        item += 1
        query = statement.format(item)
        # print(query)
        print('Status', end=':')
        print('Query',end=':')
        basebase.execute(query)
        sub_data = basebase.fetchall()
        sub_data = segmentor(sub_data)
        print('Done!')
        for segment in sub_data:
            total += 1
            counter += 1
            print("Q{}:S{}:{}/{}".format(item, total, counter, len(sub_data)), end=':')
            x, y = zip(*segment)
            x, y = array(x, dtype=float), array(y, dtype=float)
            # Set figure number
            index = chunk_size
            print('Crunching',end=':')
            while index + chunk_size < len(y) - 1:
                pyplot.scatter(x[index], avg(y[index - chunk_size:index + chunk_size]))
                index += 1
            print('Done!',end=':')
            pyplot.ylim(ylimits)
            pyplot.savefig("plot.{}.Q{}.S{}.seg_average.png".format(datetime.now(), item, total).replace(' ', '-'))
            print('Finished!')
            pyplot.close()

            
def get_fit(x, y, deg):
    """(list, list, int) -> array(y coordinates)

    Takes the x coordinates and y coordinates of the series data and the degree
    of polynomial to be used for the best fit function. Then returns the 
    calculated points in an array. These are the new corected y values."""
    with warnings.catch_warnings():
        warnings.filterwarnings('error')
        try:
            polynomial = polyfit(x, y, deg, rcond=None, full=False, w=None, cov=False)
        except RankWarning:
            while deg > 1:
                deg = deg - 1
                try:
                    polynomial = polyfit(x, y, deg, rcond=None, full=False, w=None, cov=False)
                    break
                except RankWarning:
                    if deg == 1:
                        print('+++Not enough points for linear fit.')
                        warnings.filterwarnings('always')
                        polynomial = polyfit(x, y, deg, rcond=None, full=False, w=None, cov=False)
                        break
                    else:
                        continue
    evalulate = poly1d(polynomial)
    new_data = array(evalulate(x))
    return new_data


def pull_n_graph(Database, x, y, series_type, quarter=None):
    Database.connect()
    Database.cur_gen()
    ############### THIS IS SUPER NOT OK
    if quarter == None:
        query = """SELECT {0}, {1} 
                    FROM {2}_data;""".format(x, y, series_type)
    elif quarter != None:
        query = """SELECT {0}, {1} 
            FROM {2}_data INNER JOIN {2}_defaults ON
                ({2}_data.filename = {2}_defaults.filename)
            WHERE {2}_defaults.name = 'QUARTER' 
                AND {2}_defaults.value = '{3}';""".format(x, y, series_type, quarter)
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


def show_best_fit(Database, x, y, series_type, quarter):
    ############### IMPROPER SQL ETIQUETTE
    query = """SELECT {0}, {1} 
        FROM {2}_data INNER JOIN {2}_defaults ON
            ({2}_data.filename = {2}_defaults.filename)
        WHERE {2}_defaults.name = 'QUARTER' 
            AND {2}_defaults.value = '{3}' 
            AND {0} IS NOT null 
            AND {1} IS NOT null;""".format(x, y, series_type, quarter)
    print(query)
    Database.execute(query)
    ###############
    data = Database.fetchall()
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
    pyplot.savefig("plot{}.bestfit.Q{}.png".format(datetime.now(), quarter).replace(' ', '-'))


def stitching(Database, x, y, series_type):
    # Pull Down each quarter
    pyplot.figure(figsize=(32,16), dpi=200) # 16in wide, 8in tall, 200 ppi
    # r helps generate a random color in hex
    r = lambda: random.randint(0,255)
    for quarter in range(17):
        ############### IMPROPER SQL STATEMENT
        query = """SELECT {0}, {1} 
            FROM {2}_data INNER JOIN {2}_defaults ON
                ({2}_data.filename = {2}_defaults.filename)
            WHERE {2}_defaults.name = 'QUARTER' 
                AND {2}_defaults.value = '{3}' 
                AND {0} IS NOT null 
                AND {1} IS NOT null;""".format(x, y, series_type, quarter + 1)
        print(query)
        Database.execute(query)
        ###############
        data = Database.fetchall()
        x_dat, y_dat = zip(*data)
        x_dat = array(x_dat, dtype=float)
        y_dat = array(y_dat, dtype=float)
        new_y = get_fit(x_dat, y_dat, 2)
        pyplot.scatter(x_dat,y_dat - new_y, color=('#%02X%02X%02X' % (r(),r(),r())), s=2)
    # Pulls down the x axes boundaries
    Database.execute("""SELECT MIN({0}), MAX({1}) FROM {2}_data;""".format(x, x, series_type))
    limitsX = Database.fetchall()
    pyplot.xlabel(x)
    pyplot.ylabel(y)
    pyplot.xlim(limitsX[0][0],limitsX[0][1])
    # This is an eyeballed value
    pyplot.ylim(-100,100)
    pyplot.savefig("plot{}.stitched.png".format(datetime.now(), quarter).replace(' ', '-'))
    print("FILENAME:plot{}.stitched.png".format(datetime.now(), quarter).replace(' ', '-'))


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
            # print('Step1')
            # print(tup)
            if None not in tup and len(standin) > 0 and (tup[0] == standin[-1][0] + 1):
                # print('Step2')
                standin.append(tup)
                index += 1
            elif len(standin) == 0:
                # print('Step3')
                standin.append(tup)
                index += 1  
            else:
                # print('Step4')
                if len(standin) >= 15:
                    new_data.append(standin)
                # print(new_data)
                break
    return new_data


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
            pyplot.suptitle("MIN:{} -- MAX:{} -- DIFF:{}% -- AVG:{}".format(
                round(min(y)), round(max(y)), round(((max(y) - min(y)) / min(y))*100,2), sum(y)//len(y)))
            pyplot.savefig("plot{}.seg_fit.S{}.Q{}.png".format(datetime.now(), total, item).replace(' ', '-'))
            pyplot.close()
            print(">>plot{}.seg_fit.S{}.Q{}.png".format(datetime.now(), total, item).replace(' ', '-'))


def seg_stitch(basebase, columns, quarter):
    statement = """SELECT {}, {} FROM time_data
            INNER JOIN time_defaults ON (time_data.filename = time_defaults.filename)
            WHERE time_defaults.name = 'QUARTER' 
                AND time_defaults.value = '{}';"""
    if quarter == None:
        statement = statement.format(columns[0], columns[1], "{}")
    else:
        statement = statement.format(columns[0], column[1], quarter)
    
    # 16in wide, 8in tall, 200 ppi
    pyplot.figure(figsize=(64,32), dpi=200) 
    # r helps generate a random color in hex
    r = lambda: random.randint(0,255)
    total = 0
    for item in range(17):
        color=('#%02X%02X%02X' % (r(),r(),r()))
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

            pyplot.scatter(x,y - new_y, color=color, s=2)
    pyplot.xlabel(columns[0])
    pyplot.ylabel(columns[1])
    basebase.execute("""SELECT MIN({0}), MAX({0}) FROM time_data;""".format(columns[0]))
    limitsX = basebase.fetchall()
    pyplot.xlim(limitsX[0][0],limitsX[0][1])
    # This is an eyeballed value
    pyplot.ylim(-50,50)
    pyplot.savefig("plot{}.seg_stitched.png".format(datetime.now()).replace(' ', '-'))
    print("FILENAME:plot{}.seg_stitched.png".format(datetime.now()).replace(' ', '-'))


def square_smooth(basebase, columns, to_plot=True):
 

    # columns = [x, y, smooth_width]
    width = int(columns[2])
    if width % 2 == 0:
        width = int(width / 2)
    else:
        width = int((width - 1) / 2)
    
    # Query database -> Maybe select the quarter so that it can be colored well
    query = """SELECT {}, {}
    FROM time_data;""".format(columns[0], columns[1])#INNER JOIN defaults ON (data.filename = defaults.filename);""".format(columns[0], columns[1])
    print(':Query')
    basebase.execute(query)
    all_data = basebase.fetchall()
    
    # Segment data to remove bad data
    all_data = segmentor(all_data)
    
    # Get fit for the segments
    standin = []
    total = 0 # total number of segments
    print(' -> Fitting'.format(total))
    for segment in all_data:
        total += 1
        x, y = zip(*segment) # maybe add quarter
        x, y = array(x, dtype=float), array(y, dtype=float)
        fit_y = get_fit(x, y, 2)
        corrected_y = []
        
        for index, item in enumerate(y):
            corrected_y.append(y[index] - fit_y[index])
        y = corrected_y

        standin.append(zip(x, y)) # maybe add quarter
    all_data = standin
    
    # Desegment
    all_data = desegmentor(all_data)
    all_data.sort() # sorts by x since no two are the same
    x, y = zip(*all_data) # maybe add quarter
    new_y = []
    print(' -> Rectangular Smoothing')
    
    # Smooth
    index = width + 1
    new_y.extend(y[0:index])
    total = len(y)
    # start = index
    while index < total - width:
        # start += 1
        # print("{}/{}".format(start, total))
        val = avg(y[index - width:index + width + 1], rounded=False)
        new_y.append(val)
        # print(index, val)
        index += 1
    new_y.extend(y[index:])
    
    
    if to_plot == True:
        # Plot
        # 16in wide, 8in tall, 200 ppi
        pyplot.figure(figsize=(64,32), dpi=200)
        print(' -> Plotting')
        pyplot.scatter(x, new_y, color='black', s=2)
        pyplot.suptitle('Rectangular Smoothing ({} Pts)'.format(int(columns[2])))
        pyplot.xlabel(columns[0])
        pyplot.ylabel(columns[1])
        basebase.execute("""SELECT MIN({0}), MAX({0}) FROM time_data;""".format(columns[0]))
        limitsX = basebase.fetchall()[0]
        # This is an eyeballed value
        pyplot.ylim(-45, 45)
        pyplot.xlim(limitsX[0], limitsX[1])

        name = "RectangularSmoothing.{}pt.{}.png".format(columns[2], datetime.now()).replace(' ', '-')
        pyplot.savefig(name)
        pyplot.close()
        print('-> {}'.format(name))


def triangular_smooth(basebase, columns, to_plot=True):
    # columns = [x, y, smooth_width]
    width = int(columns[2])
    if width % 2 == 0:
        width = int(width / 2)
    else:
        width = int((width - 1) / 2)
    
    # Query database -> Maybe select the quarter so that it can be colored well
    query = """SELECT {}, {}
    FROM time_data;""".format(columns[0], columns[1])#INNER JOIN defaults ON (data.filename = defaults.filename);""".format(columns[0], columns[1])
    print(':Query')
    basebase.execute(query)
    all_data = basebase.fetchall()
    
    # Segment data to remove bad data
    all_data = segmentor(all_data)
    
    # Get fit for the segments
    standin = []
    total = 0 # total number of segments
    print(' -> Fitting'.format(total))
    for segment in all_data:
        total += 1
        x, y = zip(*segment) # maybe add quarter
        x, y = array(x, dtype=float), array(y, dtype=float)
        fit_y = get_fit(x, y, 2)
        corrected_y = []
        
        for index, item in enumerate(y):
            corrected_y.append(y[index] - fit_y[index])
        y = corrected_y

        standin.append(zip(x, y)) # maybe add quarter
    all_data = standin
    
    # Desegment
    all_data = desegmentor(all_data)
    all_data.sort() # sorts by x since no two are the same
    x, y = zip(*all_data) # maybe add quarter
    new_y = []
    print(' -> Triangular Smoothing')
    
    # Smooth
    index = width + 1
    new_y.extend(y[0:index])
    total = len(y)
    # start = index
    while index < total - width:
        # start += 1
        # print("{}/{}".format(start, total))
        # val = avg(y[index - width:index + width + 1], rounded=False)
        numerator = 0
        
        fodder = y[index - width:index]
        for i, item in enumerate(fodder):
            
            numerator += (i + 1) * item
        fodder = reversed(y[index + 1:index + width + 1])
        for i, item in enumerate(fodder):
            numerator += (i + 1) * item
        
        numerator += y[index] * (width + 1)
        val = numerator / ((width + 1)  ** 2)
        new_y.append(val)
        # print(index, val)
        index += 1
    new_y.extend(y[index:])
    
    
    if to_plot == True:
        # Plot
        # 16in wide, 8in tall, 200 ppi
        pyplot.figure(figsize=(64,32), dpi=200)
        print(' -> Plotting')
        pyplot.scatter(x, new_y, color='black', s=2)
        pyplot.suptitle('Triangular Smoothing ({} Pts)'.format(int(columns[2])))
        pyplot.xlabel(columns[0])
        pyplot.ylabel(columns[1])
        basebase.execute("""SELECT MIN({0}), MAX({0}) FROM time_data;""".format(columns[0]))
        limitsX = basebase.fetchall()[0]
        # This is an eyeballed value
        pyplot.ylim(-45, 45)
        pyplot.xlim(limitsX[0], limitsX[1])

        name = "TriangularSmoothing.{}pt.{}.png".format(columns[2], datetime.now()).replace(' ', '-')
        pyplot.savefig(name)
        pyplot.close()
        print('-> {}'.format(name))
        