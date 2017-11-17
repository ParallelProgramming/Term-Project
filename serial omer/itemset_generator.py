'''
Created on 2017 M11 14

@author: omert
'''

import csv
import random

items=[21730,21754,21755,21777,22310,21756,10002,21035]#,21724,21731,21791,21883,21913,22326,22492,22540,22544,22086,20679,21068]
users = []

for i in range(20):
    users.append(random.randint(1000,2000))

output_flat = []
output_mat = []

for i in range(50):
    tid = str(random.randint(500000,700000))
    k = random.randint(1,7)
    mat_row = []
    user = str(users[random.randint(0,len(users)-1)])
    for j in range(k):
        new = False
        while (not new):
            product = str(items[random.randint(0,len(items)-1)])
            if (product not in mat_row):
                new = True
        output_flat.append([tid,product,user])
        mat_row.append(product)
    output_mat.append(mat_row)

with open('apriori_test.csv', 'w',newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    for i in range(len(output_flat)):
        csvwriter.writerow(output_flat[i])

with open('apriori_test_mat.csv', 'w',newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    for i in range(len(output_mat)):
        csvwriter.writerow(output_mat[i])

