from numpy import array
from numpy import polyfit
from numpy import zeros
from numpy import poly1d
from matplotlib import pyplot
from datetime import datetime


# For all the numerical processing & graphin functions
def get_fit(x, y, deg):
    """(list, list, int) -> array(y coordinates)

    Takes the x coordinates and y coordinates of the series data and the degree
    of polynomial to be used for the best fit function. Then returns the 
    calculated points in an array. These are the new corected y values."""
    polynomial = polyfit(x, y, deg, rcond=None, full=False, w=None, cov=False)
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
    ############### IMPROPER SQL STATEMENT
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
    pyplot.figure(figsize=(16,8), dpi=200) # 16in wide, 8in tall, 200 ppi
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
        pyplot.scatter(x_dat,y_dat - new_y, color=('#%02X%02X%02X' % (r(),r(),r())))
    # Pulls down the x axes boundaries
    Database.execute("""SELECT MIN({0}), MAX({1}) FROM {2}_data;""".format(x, x, series_type))
    limitsX = Database.fetchall()
    pyplot.xlabel(x)
    pyplot.ylabel(y)
    pyplot.xlim(limitsX[0][0],limitsX[0][1])
    # This is an eyeballed value
    pyplot.ylim(-100,100)
    pyplot.savefig("plot{}.stitched.png".format(datetime.now(), quarter).replace(' ', '-'))
