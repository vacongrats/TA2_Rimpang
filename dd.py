def mean(data):
    a=0
    a = str(round(sum(data) / len(data), 2))
    return a

data = (1,1,2,3,3,4,4,4,4)
jum = 0
jum = mean(data)
print('jum',jum)