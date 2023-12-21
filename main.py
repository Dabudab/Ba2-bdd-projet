import os


def cls():
    os.system('cls' if os.name =='nt' else 'clear')


def menu_principal():
    cls()
    print("Que souhaitez vous faire? \n")
    print("1. Ajouter une DP")
    print("2. Modifier une DP")
    print("3. Supprimer une DP")
    print("4. Analyser des DP")
    print("5. Changer de BDD")
    print("6. Montrer les DP")
    print("7. Quitter")
    try:
        choice = input("Entrez votre choix: ")
        fonctio = int(choice)

        if fonctio == 1:
            add()

        elif fonctio == 2:
            return
        elif fonctio == 3:
            return
        elif fonctio == 4:
            return
        elif fonctio == 5:
            return
        elif fonctio == 6:
            return

        elif fonctio == 7:
            exit()

        else:
            error_int = input("L'option que vous avez choisi n'existe pas")
            menu_principal()

    except ValueError:
        input("Une erreur c'est produite lors du choix (Appuyez sur Enter pour revenir au menu principal)")
        menu_principal()

def init():
    global dbh
    bdd = input("Entrez le nom du fichier contenant la BDD: ")
    menu_principal()

test = 2
def add():
    cls()
    input("Entrez le nom de la table dans laquelle vous voulez ajouter une DP: ")



    if test == 1:
        input("La table est actuellement vide (Apputez sur Enter pour revenir au menu Principal)")
        menu_principal()
    else:
        print("Veuillez séparer les différents éléments par un espace")
        gauche = input("partie gauche de la DP: ")
        droite = input("partie droite de la DP: ")
        fonctionne = 1
        if fonctionne == 1:
            erreur = input("Impossible de creer cette DP (Appuyez sur Enter pour retourner au menu principal)")
            menu_principal()

        ok = input("DP Correctement ajoutée: ")
        menu_principal()





init()