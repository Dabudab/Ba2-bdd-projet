# coding: utf-8
import sqlite3

dataBase = 'tableTest'
var1 = True
var2 = True

# Table1

table1 = 'Personne'

if var1:
    db = sqlite3.connect(dataBase)
    cursor = db.cursor()
    # creation table Personne
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Personne(NUMERO TEXT NOT NULL, PAYS TEXT NOT NULL, NOM TEXT NOT NULL, REGION TEXT NOT NULL)""")
    # insertion des donnees dans la table
    cursor.execute(""" INSERT INTO Personne(NUMERO, PAYS, NOM, REGION) VALUES(?,?,?,?)""", ("1", "BELGIQUE", "EMILE", "HAINAUT"))
    cursor.execute(""" INSERT INTO Personne(NUMERO, PAYS, NOM, REGION) VALUES(?,?,?,?)""",
                   ("2", "FRANCE", "THOMAS", "OUI"))
    # creation table FuncDep
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS FuncDep('FuncDep' TEXT NOT NULL, lhs TEXT NOT NULL, rhs TEXT NOT NULL, PRIMARY KEY('FuncDep', lhs, rhs))""")
    # insertion des DFs
    cursor.execute(""" INSERT INTO FuncDep('table', lhs, rhs) VALUES (?,?,?)""", (table1, 'NUMERO PAYS', 'NOM'))
    cursor.execute(""" INSERT INTO FuncDep('table', lhs, rhs) VALUES (?,?,?)""", (table1, 'NUMERO PAYS', 'REGION'))
    cursor.execute(""" INSERT INTO FuncDep('table', lhs, rhs) VALUES (?,?,?)""", (table1, 'REGION', 'PAYS'))


    db.commit()
    db.close()


#Table2

table2 = 'Films'

if var2:
    db = sqlite3.connect(dataBase)
    cursor = db.cursor()
    #creation table Films
    cursor.execute( """CREATE TABLE IF NOT EXISTS Films(TITRE TEXT NOT NULL, DIRECTEUR TEXT NOT NULL, ACTEUR TEXT NOT NULL, SOCIETE TEXT NOT NULL, PREMIERE TEXT NOT NULL, MINUTES TEXT NOT NULL)""")
    #insertion des données dans la table FILMS
    cursor.execute(""" INSERT INTO Films(TITRE, DIRECTEUR, ACTEUR, SOCIETE, PREMIERE, MINUTES) VALUES(?, ?, ?, ?, ?, ?)""",
                   ("The Birds", "A.Hitchcock", "T.Hedren", "Universal Pictures", "28031963", "113"))
    cursor.execute(
        """ INSERT INTO Films(TITRE, DIRECTEUR, ACTEUR, SOCIETE, PREMIERE, MINUTES) VALUES(?, ?, ?, ?, ?, ?)""",
        ("The Birds", "A.Hitchcock", "R.Taylor", "Universal Pictures", "28031963", "113"))
    cursor.execute(
        """ INSERT INTO Films(TITRE, DIRECTEUR, ACTEUR, SOCIETE, PREMIERE, MINUTES) VALUES(?, ?, ?, ?, ?, ?)""",
        ("Titanic", "J.Cameron", "K.Winslet", "Twentieth Century Fox", "19121997", "195"))
    cursor.execute(
        """ INSERT INTO Films(TITRE, DIRECTEUR, ACTEUR, SOCIETE, PREMIERE, MINUTES) VALUES(?, ?, ?, ?, ?, ?)""",
        ("Titanic", "J.Cameron", "L.DiCaprio", "Twentieth Century Fox", "19121997", "195"))
    cursor.execute(
        """ INSERT INTO Films(TITRE, DIRECTEUR, ACTEUR, SOCIETE, PREMIERE, MINUTES) VALUES(?, ?, ?, ?, ?, ?)""",
        ("The Birds", "J.Cameron", "K.Winslet", "Paramount Pictures", "28012001", "182"))
    cursor.execute(
        """ INSERT INTO Films(TITRE, DIRECTEUR, ACTEUR, SOCIETE, PREMIERE, MINUTES) VALUES(?, ?, ?, ?, ?, ?)""",
        ("The Birds", "J.Cameron", "R.Taylor", "Paramount Pictures", "28012001", "182"))

    # creation table FuncDep
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS FuncDep('table' TEXT NOT NULL, lhs TEXT NOT NULL, rhs TEXT NOT NULL, PRIMARY KEY('FuncDep', lhs, rhs))""")
    # insertion des DFs

    cursor.execute(""" INSERT INTO FuncDep('table', lhs, rhs) VALUES (?,?,?)""", (table2, 'TITRE DIRECTEUR', 'SOCIETE PREMIERE MINUTES'))

    cursor.execute(""" INSERT INTO FuncDep('table', lhs, rhs) VALUES (?,?,?)""",
                   (table2, 'DIRECTEUR PREMIERE', 'TITRE'))
    '''
    cursor.execute(""" INSERT INTO FuncDep('FuncDep', lhs, rhs) VALUES (?,?,?)""",
                   (table2, 'ACTEUR PREMIERE', 'TITRE DIRECTEUR'))
    '''
    db.commit()
    db.close()


