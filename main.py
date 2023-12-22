import os
from Data import *

def cls():
    os.system('cls' if os.name =='nt' else 'clear')


def menu_principal():
    cls()
    print("Que souhaitez vous faire? \n")
    print("1. Ajouter une DP")
    print("2. Modifier une DP")
    print("3. Supprimer une DP")
    print("4. Analyser des DP")
    print("5. Montrer les DP")
    print("6. Quitter\n")
    try:
        choice = input("Entrez votre choix: ")
        fonctio = int(choice)

        if fonctio == 1:
            add()

        elif fonctio == 2:
            modif()

        elif fonctio == 3:
            delete()

        elif fonctio == 4:
            menuAnalyse()

        elif fonctio == 5:
            show()

        elif fonctio == 6:
            cls()
            exit()

        else:
            input("L'option que vous avez choisi n'existe pas")
            menu_principal()

    except ValueError:
        input("Une erreur c'est produite lors du choix (Appuyez sur Enter pour revenir au menu principal)")
        menu_principal()

def init():
    cls()
    global dbh
    bdd = input("Bonjour, Veuillez entrez le nom du fichier contenant la Base de Données: ")
    dbh = DataBaseHandler(bdd)
    menu_principal()


def add():
    cls()
    tableName = input("Entrez le nom de la table dans laquelle vous voulez ajouter une DP: ")

    if not dbh.tabExist(tableName):
        input("La table n'existe pas (Appuyez sur Enter pour retourner au menu principal)")
        menu_principal()
    else:
        print("Veuillez séparer les différents éléments par un espace\n")
        gauche = input("partie gauche de la DP: ")
        droite = input("partie droite de la DP: ")
        dbh.addDF(tableName, gauche, droite)
        input("DP dans la table: " + tableName + ", Correctement ajoutée: "+ gauche + "->" + droite+ "\n(Appuyez sur Enter pour retourner au menu principal)")
        menu_principal()


def modif():
    cls()
    df = dbh.getDf()

    if len(df) == 0:
        input("Aucune DF présente dans la table (Appuyez sur Enter pour retourner au menu principal)")
        menu_principal()

    else:
        increment = 1
        for line in df:
            print(str(increment) + ".  Table: " + line[0] + ", DP: " + line[1] + " -> " + line[2])
            increment += 1

        nbr = input("Entrez le numéro de la DF que vous souhaitez modifier: ")
        nbr_int = int(nbr)
        if nbr_int > (len(df)) or nbr_int <= 0:
            input("la ligne que vous avez choisi n'existe pas")
            modif()

        else:
            cls()
            verif = input("Etes vous sur de vouloir modifier cette DF? (Y/N)")
            if verif == "Y" or verif == "y":
                gauche = input("Entrez les nouveaux éléments à gauche:")
                droite = input("Entrez les nouveaux éléments à droite:")
                dbh.modifDF(gauche, droite, df[nbr_int - 1][0], df[nbr_int - 1][1], df[nbr_int - 1][2])

                input("DF correctement modifiée, pour retourner au menu principal appuyez sur Enter")
                menu_principal()


            elif verif == "N" or verif == "n":
                menu_principal()

            else:
                cls()
                input("Veuillez rentrer un caractère correct")
                modif()


def delete():
    cls()

    df = dbh.getDf()

    if (len(df)) == 0:
        input("Aucune DF présente dans la table (Appuyez sur Enter pour retourner au menu principal)")
        menu_principal()

    else:
        print("Quelle DF voulez vous supprimer?")
        increment = 1
        for line in df:
            print(str(increment) + ".  Table: " + line[0] + "  DP :" + line[1] + " -> " + line[2])
            increment += 1

        try:
            num = input("Entrez le numero de la ligne : ")
            nbre = int(num)

            if nbre > (len(df)) or nbre <= 0:
                input("la ligne que vous avez choisi n'existe pas")
                delete()

            else:
                cls()
                verif = input("Etes vous sur de vouloir supprimer cette DF? (Y/N)")

                if verif == "Y" or verif == "y":
                    dbh.delDF(df[nbre - 1][0], df[nbre - 1][1], df[nbre - 1][2])
                    input("DF correctement supprimée, pour retourner au menu principal appuyez sur Enter")
                    menu_principal()

                elif verif == "N" or verif == "n":
                    menu_principal()

                else:
                    cls()
                    input("Veuillez rentrer un caractère correct")
                    delete()

        except ValueError:
            menu_principal()


def show():
    cls()
    df = dbh.getDf()

    if len(df) == 0:
        input("Aucune DF présente dans la table (Appuyez sur Enter pour retourner au menu principal)")
        menu_principal()
    else:
        increment = 1

        for line in df:
            print(str(increment) + ".  Table: " + line[0] + ", DP: " + line[1] + " -> " + line[2])
            increment += 1
        input("\nPour retourner au menu principal, appuyez sur Enter")
        menu_principal()



def menuAnalyse():
    cls()
    print("Que souhaitez vous analyser?\n")
    print("1. Montrer les DF qui ne sont pas respectées")
    print("2. Montre les DF qui sont des conséquences logiques")
    print("3. Menu Principal\n")
    try:
        choice = input("Entrez votre choix: ")
        fonctio = int(choice)

        if fonctio == 1:
            analyse()

        elif fonctio == 2:
            logic()

        elif fonctio == 3:
            menu_principal()

        else:
            input("L'option que vous avez choisi n'existe pas")
            menuAnalyse()

    except ValueError:
        input("Une erreur c'est produite lors du choix (Appuyez sur Enter pour revenir au menu principal)")
        menu_principal()



def analyse():
    cls()
    tableName = input("Veuillez entrer la table dont vous souhaitez vérifier la satisfaction des DFs: ")
    cls()
    liste = dbh.getDf()
    res = dbh.showNotActiveDP(tableName, liste)
    for ligne in res:
        print(ligne[0] + "->" + ligne[1])
    input("\nAppuyez sur Enter pour retourner au menu principal")
    menu_principal()



def logic():
    return




init()
