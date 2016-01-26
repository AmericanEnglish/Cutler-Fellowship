from database import DB
from datetime import datetime
from matplotlib import pyplot

def into_db(filename):
    current_db = DB('postgres', 'cutler', host='localhost', user='student', password='student')
    current_db.connect()
    current_db.cur_gen()
    # Saved for later debugging
    success = current_db.create_table('generate_tables.sql')
    if not success[0]:
        print(success[1])
        exit()
    # else:
    #     print('CREATED DATA TABLES')

    
    current_db.execute("""INSERT INTO files VALUES (%s, %s);""", [filename, datetime.now()])
    with open(filename, 'r') as kepler_file:
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
                current_db.execute("""INSERT INTO defaults VALUES (%s, %s, %s)""", [filename, line[0], line[1]])
            
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
                success = current_db.execute("""INSERT INTO data VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                     %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", line)
                # if not success[0]:
                #     print(success[1])
    return current_db

def graph(Database, item1, item2, quarter):
    Database.cur_gen()
    ############### THIS IS SUPER NOT OK
    query = "SELECT %s, %s FROM data;" % (item1, item2)
    print(query)
    Database.execute(query)
    ###############
    
    data = Database.fetchall()
    print(data[0:5])
    x, y = zip(*data)
    pyplot.plot(x,y)
    pyplot.savefig("plot{}.png".format(datetime.now()).replace(' ', '-'))

if __name__ == '__main__':
    from sys import argv
    graph(into_db(argv[1]), 'time', 'sap_flux')
