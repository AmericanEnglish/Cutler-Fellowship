import sqlite3
from os import listdir

stuff = listdir('./')
objs = []
for i, item in stuff:
    if "kplr" in stuff:
        print("{}:{}".format(i, item))

answer = input("Chuck(i): ")

conn = sqlite3.connect(database="Data.db")
cur = conn.cursor()
try:
    cur.execute("DROP dat;")
except:
    cur.execute("""CREATE TABLE dat (
        label lab
        label lab

        );""")
with open(stuff[i], 'r') as doc:
    # Sanatize

for index in new:
    cur.execute("""INSER INTO dat ({});""")