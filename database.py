import psycopg2
import sqlite3

class DB():
    """Used for interacting with a database by cutting down on some database
    specific interactions."""
    # Database Skeleton
    def __init__(self, db_type, db_name, host='localhost', username=None, password=None):
        self.db_type = db_type
        self.host = localhost
        self.username = username
        self.password = password
        self.con = None
        self.cur = None

    def connect(self):
        if db_type == 'sqlite3':
            self.con = sqlite3.connect(database=db_name)
            return True, None

        elif db_type == 'postgres':
            try:
                self.con = psycopg2.connect(host=host, database=db_name, user=username, password=password)
                self.password = None
                return True, None
            except psycopg2.OperationalError as err:
                return False, err

    def cur_gen(self):
        if self.cur != None:
            self.cur.close()
        self.cur = self.con.cursor()

    def commit(self):
        self.con.commit()

    def execute(self, string, arguments=None):
        if arguments == None:
            try:
                self.cur.execute(string)
                return True, None
            except psycopg2.Error as err:
                self.con.rollback()
                return False, err
        else:
            try:
                self.cur.execute(string, arguments)
                return True, None
            except psycopg2.Error as err:
                self.rollback()
                return False, err 

    def create_table(self, sqlfile):
        """(DB object, str) -> bool, str

        create_table needs to be given an SQL file. Opens, reads, and executes 
        the table creation statements. Returns a boolean and a string. The 
        boolean will indicate True if the sql creation was successful and None.
        If the table creation was not created successfully. The database is
        rolled back to the last succesful commit and then returns False as the
        bool. The string returned will be the psycopg2 error."""
        with open(sqlfile, 'r') as exe:
            try:
                # Add if statement for sqlite because it does one table at a time.
                self.execute(exe.read())
                self.commit()
                return True,  None
            except psycopg2.Error as err:
                self.rollback()
                return False, err

    def rollback(self):
        self.con.rollback()