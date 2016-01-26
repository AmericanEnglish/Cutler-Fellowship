from Crypto.Hash import SHA256
from database import DB
from datetime import datetime
from matplotlib import pyplot
from numpy import polyfit
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

def hasing(phrase):
    """(str) -> some str"""
    key = SHA256.new()
    key.update(phrase.encode(encoding='utf-8'))
    key = key.digest()
    return key

def best_fit(x, y, deg):
    return numpy.polyfit(x, y, deg, rcond=None, full=False, w=None, cov=False)

if __name__ == '__main__':
    from sys import argv
    basebase = DB('postgres', 'cutler', host='localhost', user='student', password='student')
    basebase.connect()
    basebase.cur_gen()
    if len(argv) < 3:
        success = basebase.create_table('generate_tables.sql')
        if not success[0]:
            print(success[1])
            exit()
        for item in listdir(argv[1]):
            if 'kplr' in item:
                into_db_dvseries(basebase, argv[1], item)
    else:
        graph(basebase, argv[1][:-1], argv[2][:-1], argv[3])
