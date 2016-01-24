from database import DB
from datetime import datetime
from time import sleep

def into_db(filename):
    current_db = DB('sqlite3', 'cutler.db')#, host='localhost', user='student', password='student')
    current_db.connect()
    current_db.cur_gen()
    # Just for testing
    current_db.execute("DROP TABLE data;")
    current_db.execute("DROP TABLE defaults;")
    current_db.execute("DROP TABLE files;")
    ##################
    success = current_db.create_table('../generate_tables.sql')
    if not success[0]:
        print(success[1])
        exit()
    else:
        print('CREATED DATA TABLES')
    sleep(3)

    
    current_db.execute("""INSERT INTO files VALUES (%s, %s);""", [filename, datetime.now()])
    with open(filename, 'r') as kepler_file:
        ## Remove this
        lines = kepler_file.read().count('\n')
        kepler_file.seek(0)
        temp = 0
        ## Remove ^
        for line in kepler_file:
            ##########
            temp += 1
            print("{}/{}".format(temp,lines))
            ##########

            # Handles header data
            if line[0] == """\\""":
                line = line[1:].strip().split(" = ")
                if len(line) == 1:
                    line.append('')
                print(line)
                current_db.execute("""INSERT INTO defaults VALUES (%s, %s, %s)""", [filename, line[0], line[1]])
            
            # Skips the three table headers
            elif "|" in line:
                print('skipped')
                # continue
                # line = line[1:-1].replace("|"," ").split()
            
            # Handles the EOF and perhaps bizzare line breaks
            elif len(line) < 5:
                continue
            # The important stuff
            else:
                # Insert data into the database
                line = line.split()
                for index, item in enumerate(line):
                    if item == 'null':
                        line[index] = None
                    elif '.' not in item:
                        line[index] = int(item)
                    else:
                        line[index] = float(item)
                line.insert(0, filename)
                print(line)
                # Shove it into the database
                success = current_db.execute("""INSERT INTO data VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                     %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", line)
                if not success[0]:
                    print(success[1])



if __name__ == '__main__':
    from sys import argv
    print(argv)
    into_db(argv[1])
    print('Completed')
