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
            if line[0] == "\\":
                # Do stuff
                if "KEPLERID" == line[0]:
                    kep_id = line[1]
                elif "QUARTER" == line[0]:
                    quarter = line[1]
            elif line[0] == "|":
                # Do stuff
            elif len(line) < 5:
                continue
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
