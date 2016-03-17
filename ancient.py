from Crypto.Hash import SHA256
from database import DB
from datetime import datetime
from matplotlib import pyplot
from numpy import polyfit
from numpy import poly1d
from numpy import array
from numpy import zeros
from os import listdir
from os.path import isdir
from os.path import isfile
from clean import *
from processing import *
import random
import warnings


def trim_segments(basebase, columns):
    data = segmentor(data)
    trimmed = []
    for segment in data:
        trimmed.append(trim(segment, 5))


def trim(seg_data, percent):
    """(list of seg data) -> list of trimmed seg data

    Takes a list of pre segmented data and then returns a trimmed version of 
    that data using the percent. The operates under the assumptions that follow:

    1. Data will be fit with a line. 
    2. Data beyond the line five percent line will be trimmed
    3. The trimmed data will be returned [(num, num, num,), (num,num,num)]"""
    percent = 5/100.
    # Initial fit
    x, y = zip(*segment)
    new_y = get_fit(x, y, 2)
    trimmed_x = []
    trimmed_y = []
    for index, tup in enumerate(zip(y, new_y)):
        # This creates the artificial band
        if not ((tup[0] > (tup[1] + tup[1]*percent)) and (tup[0] < (tup[1] - tup[1]*percent))):
            trimmed_x.append(x[index])
            trimmed_y.append(tup[0])
        # Get a fit for the new data
        new_y = get_fit(trimmed_x, trimmed_y, 2)
        # Zip it back up
        new_segments.append(zip())


    # 5% trimming
    # New fit