from itertools import groupby
from operator import itemgetter
data = [ 1, 4,5,6, 10, 15,16,17,18, 22, 25,26,27,28]
alist=[]
for k, g in groupby(enumerate(data), lambda x:x[0]-x[1]):
    alist.append(list(map(itemgetter(1), g)))

new_list=[x for x in alist if len(x)>=3]

print(new_list)