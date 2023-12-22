import sqlite3
import os, itertools,copy
from typing import Any

class DataBaseHandler:

    def __init__(self, table_name:str):
        self.table=table_name
        self.connection=sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{self.table}")
        self.cursor=self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS FuncDep('table' TEXT NOT NULL, lhs TEXT NOT NULL, rhs TEXT NOT NULL, PRIMARY KEY('table', lhs, rhs))""")
        self.connection.commit()

    def addDF(self,table, lhs, rhs):
        query= f"""INSERT INTO FuncDep('table', lhs, rhs) VALUES ('{table}','{lhs}','{rhs}');"""
        self.cursor.execute(query)
        self.connection.commit()
        
    def delDF(self,table ,lhs,rhs):
        query=f"""DELETE FROM FuncDep WHERE FuncDep.'table'=? AND lhs=? AND rhs=?"""
        self.cursor.execute(query,(table,lhs,rhs),)
        self.connection.commit()

    def getDf(self):
        retour=[]
        query="""SELECT * FROM FuncDep"""
        self.cursor.execute(query)
        for items in self.cursor:
            l=[]
            for elements in items:
                l.append(elements)
            retour.append(l)
        return retour
    
    def CandidateKey(self, table, key):
        query=f"""SELECT rhs from FuncDep WHERE FuncDep.'table'=?"""
        self.cursor.execute(query,(table))
        retour=[]
        for items in self.cursor:
            l=[]
            for elements in items:
                l.append(elements)
            if key not in l[2]:
                return True
            if key not in l[1]:
                return False
            
    
    
    def getKey(self,table):
        generate,left_candidate,righ_candidate,alllist=self.getAttribute(table) 
        keys=[]
        for i in range(1,len(left_candidate)+1):
            for comb in itertools.combinations(left_candidate,i):
                base = list(comb)
                flagp=True
                while(flagp):
                    flagp=False
                    if len(base)==len(generate):
                        keys.append(list(comb))
                        break
                    for j in range(len(alllist)):
                        l=alllist[j][0]
                        if len(l)>1:
                            p=l.split(" ")
                            flag=True
                            for e in p:
                                if e not in base:
                                    flag=False
                                    break
                            if flag and alllist[j][1] not in base:
                                base.append(alllist[j][1])
                                flagp=True
                        else:
                            if l in base and alllist[j][1] not in base:
                                base.append(alllist[j][1])
                                flagp=True
    
        validkeys=[]
        validkeys=copy.deepcopy(keys)
        for i in range(len(keys)-1):
            for j in range(i+1,len(keys)):
                if  keys[j] in validkeys and set(keys[i])<=set(keys[j]) :            
                    validkeys.remove(keys[j])

        return validkeys

    def getAttribute(self,table):
        query=f"""SELECT * from FuncDep WHERE FuncDep.'table'=?"""
        self.cursor.execute(query,(table,))
        dumpdb=self.cursor.fetchall()
        left_candidate=[]
        right_candidate=[]
        generate=[]
        dfdic=[]
        for line in dumpdb:
            name, lhs, rhs=line
            dfdic.append([lhs,rhs])
            if " " in lhs:
                temp=lhs.split(" ")
                for c in temp:
                    if c not in left_candidate:
                        left_candidate.append(c)
            else:
                if lhs not in generate:
                    left_candidate.append(lhs)
        
            if " " in rhs:
                temp=rhs.split(" ")
                for c in temp:
                    if c not in right_candidate:
                        right_candidate.append(c)
            else:
                if rhs not in right_candidate:
                    right_candidate.append(rhs)
        
        generate= list(set(left_candidate+right_candidate))
        return generate,left_candidate,right_candidate,dfdic
    
    
    def is3NF(self,table):
        """
            Regarde si tous les attributs dépendants sont premiers sinon, vérifie que chaque élément
            dépend d'une clé candidate.
        """

        keys=self.getKey(table)
        attributes, lhs, rhs, dfdic=self.getAttribute(table)
        baddf=[]
        count=0
        flag=True
        #Verifie si tous les attributs dépendants sont premiers.
        for key in keys:
            for r in rhs:
                if r in key:
                    count+=1
                    break
        if count==len(rhs):
            return baddf
        #Verifie que chaque attribut de la partie gauche d'une DF est une clé.
        else:  
            for j in range(len(dfdic)):
                l=dfdic[j][0]
                if " " in l:
                    temp=l.split(" ")
                if temp not in keys:
                    baddf.append([l,dfdic[j][1]])
                    flag=False          
        if not flag:
                return baddf
        return baddf
                    

    def isBCNF(self,table):
        """
            Vérifie si la table est en 3NF, sinon forcément pas en BCNF, si oui il faut vérifier
            que chaque dépendance repose sur une clé candidate.
        """
        baddf=self.is3NF(table)
        #SI TABLE PAS EN 3NF ALORS PAS EN BCNF
        if len(baddf) != 0:
            return baddf
        
        #SI ATTRIBUT DEPEND D'AUTRE CHOSE QUE DE LA CLE ALORS TABLE PAS EN BCNF
        else:
            flag=True
            baddf=[]
            keys=self.getKey(table)
            attributes, lhs, rhs, dfdic=self.getAttribute(table)
            for j in range(len(dfdic)):
                l=dfdic[j][0]
                if " " in l:
                    temp=l.split(" ")
                    if temp not in keys:
                        baddf.append([l,dfdic[j][1]])
                        flag=False  
                elif l not in keys:
                    baddf.append([l,dfdic[j][1]])
                    flag=False       
        if not flag:
                return baddf
        return baddf


                
            
    
    


        
  