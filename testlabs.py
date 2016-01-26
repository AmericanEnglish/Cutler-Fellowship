from database import DB
from datetime import datetime
from matplotlib import pyplot
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


def into_db_DVseries(Database, filename):
    pass

def query_builder(arguments):
    """(dict of strs) -> str

        Takes a dictionary of arguments and constructs and SQL query to be fed
        into a database. Below is a bare minimum dictionary required.

        sample = {
            x:'x_name',
            y:'y_name',
            series_type:'time/DV'
        }
        >>> query_builder(sample)
        'SELECT x_name, y_name FROM time/DV_data;"""


if __name__ == '__main__':
    from sys import argv
    basebase = DB('postgres', 'cutler', host='localhost', user='student', password='student')
    print(basebase)
    basebase.connect()
    basebase.cur_gen()
    if len(argv) < 3:
        create_tables(basebase, 'generate_tables.sql')
        for item in listdir(argv[1]):
            if 'kplr' in item:
                into_db_timeseries(basebase, argv[1], item)
    else:
        graph(basebase, argv[1][:-1], argv[2][:-1], argv[3])
