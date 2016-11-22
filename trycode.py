import csv
import pprint

with open('/home/vphrase/Desktop/subha.csv') as csvfile:
    reader=csv.DictReader(csvfile,delimiter=',')
    pprint.PrettyPrinter()
    pprint.pprint(list(reader))
