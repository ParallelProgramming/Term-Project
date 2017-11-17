'''
Created on 2017 M11 16

@author: omert
'''
import csv
filename = "retail.dat"
output_file = "reatil.csv"
file_read = open(filename,"r")
output=[]
tid=0
for line in file_read:
    objects = line.split(" ")
    for item in objects:
        if (item.isdigit()):
            output.append([tid,item])
    tid+=1
file_read.close()

with open(output_file,"w",newline="") as csvfile:
    writer = csv.writer(csvfile,delimiter=',')
    for record in output:
        writer.writerow(record)
