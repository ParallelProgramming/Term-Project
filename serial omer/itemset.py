'''
Created on 2017 M11 14

@author: omert
'''
class Itemset:
    
    def __init__(self,item,index,transactions,support):
        self.keys = item
        self.indexes = index
        self.data = transactions
        self.support = support
    
    def set_support(self,support):
        self.support = support
    
    def __str__(self):
        output = "items=[({},{})".format(self.keys[0],self.indexes[0])
        for i in range(1,len(self.keys)):
            output+=",({},{})".format(self.keys[i],self.indexes[i])
        output += "], support={}".format(self.support)
        #output += "]\n({}".format(self.data[0])
        #for i in range(1,len(self.data)):
        #    output += ",{}".format(self.data[i])
        #output+= ")"
        return output
            