from database import DB
from datetime import datetime

def into_db(filename):
    current_db = DB('sqlite3', 'testing.db')
    current_db.connect()
    current_db.cur_gen()
    # Just for testing
    # current_db.execute("DROP TABLE data;")
    # current_db.execute("DROP TABLE defaults;")
    # current_db.execute("DROP TABLE files;")
    ##################
    current_db.create_table('../generate_tables.sql')
    
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
                ##########
                print(line)
                ##########
                if "KEPLERID" == line[0]:
                    kep_id = line[1]
                elif "QUARTER" == line[0]:
                    quarter = line[1]
            # Skips the three table headers
            elif "|" in line:
                continue
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
                # Places kepler id and quarter value for the data point
                line.insert(0, quarter)
                line.insert(0, kep_id)
                # Shove it into the database
                current_db.execute("""INSERT INTO data VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                     %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", line)



if __name__ == '__main__':
    from sys import argv
    print(argv)
    into_db(argv[1])
    print('Completed')
