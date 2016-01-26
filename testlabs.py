from database import DB
from datetime import datetime
from matplotlib import pyplot

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
