import csv

with open('/home/vphrase/Desktop/subha.csv') as csvfile:
    reader=csv.reader(csvfile,delimiter=',')
    header=reader.__next__()
    #print(header)
    for row in reader:
        print(row)
