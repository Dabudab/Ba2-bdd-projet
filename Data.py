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


    def showNotActiveDP(self, tableName, liste):
        print("Liste des DFs de la base de données: \n")
        for elements in liste:
            print("Table: " + elements[0] + ", " + elements[1] + " -> " + elements[2])
        print("\n")
        res = []
        for tuples in liste:
            if tuples[0] == tableName:
                res.append(tuples)

        print("Liste des DFs de la table" + tableName + ": \n")
        for lignes in res:
            print(lignes[1] + " -> " + lignes[2])
        print("\n")

        print("Liste des DF pour la table " + tableName + " qui ne sont pas satisfaites: \n")
        dfs = []
        for ligne in res:
            dp = self.isDFActive(ligne[0], ligne[1], ligne[2])
            if dp is not None:
                dfs.append(dp)

        return dfs

    def isDFActive(self, tableName, lhs, rhs):
        if type(lhs) == str:
            newLhs = lhs.split()

        query = "SELECT t1.*, t2." + rhs + " FROM " + tableName + " t1, " + tableName + " t2 WHERE "
        for attributes in newLhs:
            query += "t1." + attributes + " == t2." + attributes + " AND "
        query += "t1." + rhs + " != t2." + rhs
        self.cursor.execute(query)

        res = []

        for tuples in self.cursor:
            line = []
            for item in tuples:
                line.append(item)
            line.pop()
            res.append(line)
        if len(res) != 0:
            return tableName, lhs, rhs

    def tabExist(self, tableName):
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        dbh = self.cursor.execute(query)
        res = []
        for lignes in dbh:
            res.append(lignes)

        flag = False
        for ligne in res:
            if tableName in ligne:
                return True
        return flag

    def isLogic(self, table, lhs, rhs, remove):
        if self.dpExist(table, lhs, rhs):
            res = self.getDf()
            ens = []
            for ligne in res:
                if ligne[0] == table:
                    ens.append(ligne)
            if remove:
                ens.remove([table, lhs, rhs])
            result = self.fermeture(ens, lhs.split())

            return rhs in result
        else:
            return None

    def getLogicDP(self, table):
        allDF = self.getDf()
        res = []
        for ligne in allDF:
            if ligne[0] == table:
                res.append(ligne)
        logic = []
        for dep in res:
            if self.isLogic(dep[0], dep[1], dep[2], True):
                logic.append(dep)

        return logic

    def dpExist(self, table, lhs, rhs):
        res = self.getDf()
        for ligne in res:
            if ligne[0] == table and ligne[1] == lhs and ligne[2] == rhs:
                return True
        return False

    def fermeture(self, DF, attribute):

        closure = copy.deepcopy(DF)
        newDP = copy.deepcopy(attribute)
        oldDP = None

        while oldDP != newDP:
            oldDP = copy.deepcopy(newDP)
            for items in closure:
                a = items[1]
                b = items[2]

                if self.isIn(a.split(), newDP):
                    if b not in newDP:
                        newDP.append(b)
        return newDP

    def isIn(self, small, big):

        for sItem in small:
            sItemIsInBig = False
            for bItem in big:
                if sItem == bItem:
                    sItemIsInBig = True
            if sItemIsInBig == False:
                return False
        return True

            
    
    
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


                
            
    
    


        
  