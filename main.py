# coding: utf-8
from Data import *

f=DataBaseHandler('delTest')

def printDf():
    nb=1
    df=f.getDf()
    for line in df:
        print(str(nb)+".  Table: "+line[0]+"  dependance fonctionnelle: "+line[1]+" --> "+line[2])
        nb+=1

"""f.addDF("overflow","A","B")
f.addDF("overflow","E D","A")
f.addDF("overflow","B C","E")
f.addDF("tableTest", "Jean", "Génie")"""
printDf()
f.getKey("overflow")
    
