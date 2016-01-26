from database import DB
from datetime import datetime
from matplotlib import pyplot
from clean import into_db
def graph(Database, x, y, quarter):
    Database.connect()
    Database.cur_gen()
    ############### THIS IS SUPER NOT OK
    query = """SELECT {}, {} 
            FROM data INNER JOIN defaults ON
                (data.filename = defaults.filename)
            WHERE defaults.name = 'QUARTER' 
                AND defaults.value = %s;""".format(x, y)
    Database.execute(query, (quarter,))
    ###############
    
    data = Database.fetchall()
    x, y = zip(*data)
    pyplot.plot(x,y)
    pyplot.xlabel(x)
    pyplot.ylabel(y)
    pyplot.savefig("plot{}.png".format(datetime.now()).replace(' ', '-'))

if __name__ == '__main__':
    from sys import argv
    graph(DB('postgres', 'cutler', host='localhost', user='student', password='student'), 'time', 'sap_flux', '2')
