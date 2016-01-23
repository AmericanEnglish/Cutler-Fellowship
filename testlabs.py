from database import DB
from datetime import datetime
def into_db(filename):
    current_db = DB('sqlite', 'testing.db')
    current_db.connect()
    current_db.cur_gen()
    with open('generate_tables.sql', 'r') as create:
        current_db.create_table(create.read())
    
    current_db.insert("""INSERT INTO files VALUES (%s, %s);""", [filename, datetime.now()])
    with open(filename, 'r') as kepler_file:
        for line in kepler_file:
            # Handles header data
            if line[0] == "\\":
                line = line[1:].split("=")
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
                line.insert(0, quarter)
                line.insert(0, kep_id)
                current_db.insert("""INSERT INTO data VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                     %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", line)



if __name__ == '__main__':
    from sys import argv
    into_db(argv[1])
    print('Completed')
