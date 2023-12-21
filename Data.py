import sqlite3
import os

class DataBaseHandler:

    def __init__(self, table_name:str):
        self.table=table_name
        self.connection=sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{self.table}")
        self.cursor=self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS FuncDep('table' TEXT NOT NULL, lhs TEXT NOT NULL, rhs TEXT NOT NULL, PRIMARY KEY('table', lhs, rhs))""")
        self.connection.commit()

    def addDF(self, lhs, rhs):
        query= f"""INSERT INTO FuncDep('table', lhs, rhs) VALUES ('{"FuncDep"}','{lhs}','{rhs}');"""
        self.cursor.execute(query)
        self.connection.commit()
        
    def delDF(self, rhs):
        query=f"""DELETE FROM FuncDep WHERE rhs='{rhs}'"""
        self.cursor.execute(query)
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
    
        
        
