'''
Created on 2017 M11 14

@author: omert
'''
import sys
import csv
import itertools
import datetime
from _operator import itemgetter
from itemset import Itemset
from arule import Association_Rule
from _pickle import load

def import_data(filename):
    output_list = []
    with open(filename, 'r') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',')
        for row in datareader:
            output_list.append((row[0],row[1]))
    return output_list

def unique_transactions(data):
    data.sort(key=itemgetter(0))
    curr_tid = data[1][0]
    prev_tid = data[0][0]
    counter = 0
    for i in range(2,len(data)):
        if (curr_tid!=prev_tid):
            counter+=1
        prev_tid = curr_tid
        curr_tid = data[i][0]
    return counter

def split_sort(data,total_items):
    output = []
    data.sort(key=itemgetter(1,0))
    index = 0
    item_counter=0
    while (index<len(data)):
        curritem = []
        item = data[index][1]
        while(index<len(data) and item==data[index][1]):
            curritem.append(data[index][0])
            index+=1
        output.append(Itemset([item],[item_counter],curritem,support(curritem, total_items)))
        item_counter+=1
    return output

def item_keys_union(item1,item2):
    new_indexes=[]
    new_keys=[]
    i1=0
    i2=0
    while(i1<len(item1.indexes) and i2<len(item2.indexes)):
        if (item1.indexes[i1]==item2.indexes[i2]):
            new_indexes.append(item1.indexes[i1])
            new_keys.append(item1.keys[i1])
            i1+=1
            i2+=1
        elif (item1.indexes[i1]<item2.indexes[i2]):
            new_indexes.append(item1.indexes[i1])
            new_keys.append(item1.keys[i1])
            i1+=1
        else:
            new_indexes.append(item2.indexes[i2])
            new_keys.append(item2.keys[i2])
            i2+=1
    while(i1<len(item1.indexes)):
        new_indexes.append(item1.indexes[i1])
        new_keys.append(item1.keys[i1])
        i1+=1
    while(i2<len(item2.indexes)):
        new_indexes.append(item2.indexes[i2])
        new_keys.append(item2.keys[i2])
        i2+=1
    return new_indexes,new_keys

def item_data_union(item1,item2):
    output_set = []
    i1 = 0
    i2 = 0
    while (i1<len(item1.data) and i2<len(item2.data)):
        if (item1.data[i1]==item2.data[i2]):
            output_set.append(item1.data[i1])
            i1+=1
            i2+=1
        elif (item1.data[i1]<item2.data[i2]):
            i1+=1
        else:
            i2+=1
    
    return output_set       

def support(data,total_items):
    s = len(data)/total_items
    return s


def support_filter(set,t):
    output = []
    for i in range(len(set)):
        if (set[i].support>=t):
            output.append(set[i])
    return output

def list_to_key(lst):
    key = str(lst[0])
    for i in range(1,len(lst)):
        key+=","+str(lst[i])
    return key



def calc_confidence_lift(itemset,support_vector,conf):
    rules_vector={}
    for item in itemset:
        keys = item.keys
        support = item.support
        for i in range(1,len(keys)):
            for perm in itertools.combinations(keys, i):
                a = list(perm)
                a_key = list_to_key(a)
                b = [item for item in keys if item not in list(a)]
                b_key = list_to_key(b)
                new_key = a_key + "->" + b_key
                if new_key not in rules_vector:
                    support_a = support_vector[a_key]
                    support_b = support_vector[b_key]
                    confidence = support / support_a
                    lift = support / (support_a*support_b)
                    if confidence > conf:
                        rules_vector[new_key] = Association_Rule(a,b,support,confidence,lift)
    return rules_vector
                    
            
        
def a_priori(data,total_items,s,c):
    output_set = []
    curr_set = data
    k=1
    support_vector={}
    while len(curr_set)>0:
        new_set=[]
        added_indexes=[]
        filtered = support_filter(curr_set,s)
        for i in range(len(filtered)):
            if(k>1):
                output_set.append(filtered[i])
            support_vector[list_to_key(filtered[i].keys)] = filtered[i].support
        k+=1
        for i in range(len(filtered)):
            for j in range(i+1,len(filtered)):
                new_indexes,new_keys = item_keys_union(filtered[i], filtered[j])
                if (len(new_indexes)==k and new_indexes not in added_indexes):
                    new_data = item_data_union(filtered[i], filtered[j])
                    new_set.append(Itemset(new_keys,new_indexes,new_data,support(new_data, total_items)))
                    added_indexes.append(new_indexes)
        curr_set = new_set
    return calc_confidence_lift(output_set,support_vector,c)
        


def main():
    total_time = 0
    for i in range(10):
        #filename = "reatil.csv"
        filename = "online_retail_full.csv"
        start_time = datetime.datetime.now()
        support = 0.02 #sys.argv[0]
        confidence = 0.6
        input = import_data(filename)
        load_time = datetime.datetime.now()
        print("Took {} to load data".format(load_time - start_time))
        total_transactions = unique_transactions(input)
        print("Total transactions={}".format(total_transactions))
        data = split_sort(input,total_transactions)
        sort_time = datetime.datetime.now()
        print("Took {} to sort data".format(sort_time - load_time))
        print("Assocaition rules:")
        rules = a_priori(data, total_transactions,support,confidence)
        calc_time = datetime.datetime.now()
        for r in rules.values():
            print(r)
        print("Found {} rules".format(len(rules.values())))
        print("Took {} to calc rules".format(calc_time - sort_time))
        print("Took {} in total".format(datetime.datetime.now() - start_time))
        time_d = datetime.datetime.now() - start_time
        total_time += time_d.total_seconds()
    print ("Average time is {}".format(total_time/10))

    
main()