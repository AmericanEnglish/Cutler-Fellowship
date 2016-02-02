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
    new_data = zeros((1,len(x)))
    
    index = 0
    for item in x:
        new_data[index] = evalulate(item)

    return new_data

def pull_n_graph(Database, x, y, series_type, quarter=None):
    Database.connect()
    Database.cur_gen()
    ############### THIS IS SUPER NOT OK
    if quarter == None:
        query = """SELECT {0}, {1} 
                    FROM {2}_data;""".format(x, y, series_type)
    elif quarter != None:
        """SELECT {0}, {1} 
            FROM {2}_data INNER JOIN {2}_defaults ON
                ({2}_data.filename = {2}_defaults.filename)
            WHERE {2}_defaults.name = 'QUARTER' 
                AND {2}_defaults.value = {3};""".format(x, y, series_type, quarter)
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