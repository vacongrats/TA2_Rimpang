import math


def mean(data):
    a = str(round(sum(data) / len(data), 2))
    return a

def variance(data, ddof=0):
    n = len(data)
    mean = sum(data)/n
    return sum((x - mean)**2 for x in data)/ (n - ddof)

def stdev(data):
    var = variance(data)
    std_dev = math.sqrt(var)
    return std_dev

data =(85, 90, 70, 95, 91)
print('std :',stdev(data))
print ('mean :',mean(data))
