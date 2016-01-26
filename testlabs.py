from database import DB
from datetime import datetime
from matplotlib import pyplot
from Crypto import SHA256, Random
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


def into_db_DVseries(current_db, directory, filename):
    current_db.cur_gen()
    # Saved for later debugging
    # else:
    #     print('CREATED DATA TABLES')

    
    current_db.execute("""INSERT INTO files VALUES (%s, %s);""", [filename, datetime.now()])
    with open("{}{}".format(directory, filename), 'r') as kepler_file:
        for line in kepler_file:
            # Handles header data
            if line[0] == "\\":
                line = line[1:].strip().split(" = ")
                if len(line) == 1:
                    line.append('')
                # Removes the double string formatting that can be present
                if line[1].count("'") == 2:
                    line[1] = line[1][1:-1]
                # Cleans up extra spacing that may exist
                for index, item in enumerate(line):
                    line[index] = item.strip()
                # print(line)
                current_db.execute("""INSERT INTO time_defaults VALUES (%s, %s, %s)""", [filename, line[0], line[1]])
            
            # Skips the three table headers
            elif "|" in line:
                continue
            
            # Handles the EOF and perhaps bizzare line breaks
            elif len(line) < 5:
                continue
            # The important stuff
            else:
                # Insert data into the database
                line = line.split()
                # Sanatize read data for insertion
                for index, item in enumerate(line):
                    if item == 'null':
                        line[index] = None
                    elif '.' not in item:
                        line[index] = int(item)
                    else:
                        line[index] = float(item)
                # Get the filename in there
                line.insert(0, filename)
                # Shove it into the database
                success = current_db.execute("""INSERT INTO time_data VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                     %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", line)
                if not success[0]:
                    print(success[1])
    return current_db

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
    """(str) -> AES, byte object""")
    key = SHA256.new()
    key.update(phrase.encode(encoding='utf-8'))
    key = key.digest()
    return key

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
