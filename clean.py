from datetime import datetime
from database import DB
import psycopg2
import sqlite3


# Cleaning & Converting Production File
def hash(phrase):
    """(str) -> bytes"""
    key = SHA256.new()
    key.update(phrase.encode(encoding='utf-8'))
    key = key.hexdigest()
    return key

    
def into_db_timeseries(current_db, directory, filename):
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


def into_db_dvseries(current_db, directory, filename):
    current_db.cur_gen()
    # Saved for later debugging
    # else:
    #     print('CREATED DATA TABLES')

    
    current_db.execute("""INSERT INTO files VALUES (%s, %s);""", [filename, datetime.now()])
    with open("{}{}".format(directory, filename), 'r') as kepler_file:
        for line in kepler_file:
            # Handles header data
            if line[0] == "\\":
                if "=" not in line:
                    continue
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
                current_db.execute("""INSERT INTO dv_defaults VALUES (%s, %s, %s)""", [filename, line[0], line[1]])
            
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
                    if item == 'NaN':
                        line[index] = None
                    elif '.' not in item:
                        line[index] = int(item)
                    else:
                        line[index] = float(item)
                # Get the filename in there
                line.insert(0, filename)
                # Shove it into the database
                success = current_db.execute("""INSERT INTO dv_data VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s);""", line)
                if not success[0]:
                    print(success[1])
    return current_db


def create_tables(database, tablesql):
    database = DB('postgres', 'cutler', host='localhost', user='student', password='student')
    database.cur_gen()
    database.create_table(tablesql)
    return database


def rip_to_local(basebase, columns, quarter=None):
    """Dumps segmented data into the current working directory."""
    select = ""
    for item in columns:
        select += "{}, ".format(item)
    select = select[:-2]
    if quarter != None:
        # Select Quarter data
        # Parse
        pass
    else:
        query = """SELECT {} FROM time_data
            INNER JOIN time_defaults ON (time_data.filename = time_defaults.filename)
            WHERE time_defaults.name = 'QUARTER' 
                AND time_defaults.value = '{}';"""
        # For loops over range parsing
        counter = 0
        for quarterno in range(17):
            statement = query.format(select, quarterno + 1)
            print(statement)
            basebase.execute(statement)
            filename = './kplrID_S{}_Q{}.csv'.format('{}', quarterno + 1)
            data = basebase.fetchall()
            index = 0
            while index < len(data) - 1:# using the tracked list index
                while None in data[index]:
                    index += 1
                counter += 1
                with open(filename.format(counter), 'w') as new_file:
                    new_file.write((("{},"*len(columns))[:-1] +"\n").format(*columns))
                    for tup in data[index:]:
                        if None not in tup:
                            # The perfect csv write string
                            new_file.write((("{},"*len(tup))[:-1] +"\n").format(*tup))
                            index += 1
                        else:
                            break
