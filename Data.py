import sqlite3
import os, itertools,copy

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

    def modifDF(self, lhs, rhs, table, oldlhs, oldrhs):
        self.cursor.execute('''UPDATE FuncDep SET lhs = ?, rhs = ? WHERE FuncDep.'table' = ? AND lhs = ? AND rhs = ?''',
                            (lhs, rhs, table, oldlhs, oldrhs))
        self.connection.commit()
    
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
        query=f"""SELECT * from FuncDep WHERE FuncDep.'table'=?"""
        self.cursor.execute(query,(table,))
        dumpdb=self.cursor.fetchall()
        left_candidate=[]
        right_candidate=[]
        candidate=[]
        alllist={}
        for line in dumpdb:
            name, lhs, rhs=line
            alllist[lhs]=rhs
            if " " in lhs:
                temp=lhs.split(" ")
                for c in temp:
                    if c not in left_candidate:
                        left_candidate.append(c)
            else:
                if lhs not in candidate:
                    left_candidate.append(lhs)
        
            if " " in rhs:
                temp=rhs.split(" ")
                for c in temp:
                    if c not in right_candidate:
                        right_candidate.append(c)
            else:
                if rhs not in candidate:
                    right_candidate.append(rhs)
        print(left_candidate, right_candidate)
        
        candidate= list(set(left_candidate+right_candidate)) 
        
        keys=[]
        for i in range(1,len(left_candidate)+1):
            for comb in itertools.combinations(left_candidate,i):
                base = list(comb)
                flagp=True
                while(flagp):
                    flagp=False
                    if len(base)==len(candidate):
                        keys.append(comb)
                        break
                    for l in alllist.keys():
                        if len(l)>1:
                            p=l.split(" ")
                            flag=True
                            for e in p:
                                if e not in base:
                                    flag=False
                                    break
                            if flag and alllist[l] not in base:
                                base.append(alllist[l])
                                flagp=True
                        else:
                            if l in base and alllist[l] not in base:
                                base.append(alllist[l])
                                flagp=True
    
        validkeys=[]
        validkeys=copy.deepcopy(keys)
        for i in range(len(keys)-1):
            for j in range(i+1,len(keys)):
                if  keys[j] in validkeys and set(keys[i])<=set(keys[j]) :            
                    validkeys.remove(keys[j])
                    
                    



        




            
    
    


        
