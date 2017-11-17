import csv

transactions = {}
filename = "reatil.csv"
with open(filename, 'r') as csvfile:
    datareader = csv.reader(csvfile, delimiter=',')
    for row in datareader:
        if (row[0] in transactions):
            transactions[row[0]].append(row[1])
        else:
            transactions[row[0]] = [row[1]]

test_values=['110','38']

counter=0
for k in transactions.keys():
    all_found=True
    i=0
    while(all_found and i<len(test_values)):
        if (test_values[i] in transactions[k]):
            i+=1
        else:
            all_found=False
    if (all_found):
        counter+=1

print("{} are found in {} out of {}".format(test_values,counter,len(transactions.keys())))