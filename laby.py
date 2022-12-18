# Importation des modules
import turtle as t
import random as rd
from tkinter import *
from tkinter.messagebox import askyesno
from os import listdir
from os.path import isfile, join
from lireLaby import labyFromFile
import time as tm

# Configuration de la fenêtre
screen = t.Screen()
# On définit le 0,0 en haut à gauche de la feneêtre pour éviter les coordonées négatives !
screen.setup(1200, 800)
screen.setworldcoordinates(
    0, screen.window_height(), screen.window_width(), 0)
screen.title("Labyrinthe")

screen.update()

# Création de dicoJeu, qui contient toutes les variables globales
dicoJeu = {"debug": True, "taille_mur": 50,
           "spawn": (100, 100), "running": False}
chemin_parcouru = []
chemin = []
grille = None

# FONCTIONS DU SUJET ET AUTRES FONCTIONS POUR LA PARTIE - TURTLE


def afficheGraphique(dicoJeu, epaisseur=0, fichier=None):
    '''
    Affiche le labyrinthe dans une fenêtre graphique.
    ---
    laby: liste des valeurs du labyrinthe
    epaisseur: épaisseur des murs
    '''
    x_spawn, y_spawn = dicoJeu["spawn"]
    taille_mur = dicoJeu["taille_mur"]

    if fichier == None:
        laby = dicoJeu["laby"]
        entree = dicoJeu["entree"]
        sortie = dicoJeu["sortie"]
    else:
        file1 = labyFromFile(fichier)
        laby = file1[0]
        entree = file1[1]
        sortie = file1[2]

    # Initialisation de la tortue
    t.reset()
    t.update()
    t.tracer(0)
    t.up()
    t.goto(x_spawn, y_spawn)
    t.down()
    t.pensize(epaisseur)
    t.shapesize(3)

    # Parcours du labyrinthe
    for ligne in range(len(laby)):
        for v in range(len(laby[ligne])):
            if [ligne, v] == entree:
                tracerCarré("red")
            elif [ligne, v] == sortie:
                tracerCarré("blue")
            elif laby[ligne][v] == 1:
                tracerCarré("gray")

            # On avance à la case suivante
            t.up()
            t.forward(taille_mur)
            t.down()

        # Retour à la ligne
        t.up()
        t.goto(x_spawn, t.ycor() + taille_mur)
        t.down()
    t.up()

    t.hideturtle()
    t.update()
    t.tracer(1)


def genererLabyAleatoire():
    '''
    Génère un labyrinthe aléatoire.
    '''
    # Variables impaires seulement
    hauteur = 11
    largeur = 17
    # Création du labyrinthe vide
    laby = [[] for i in range(hauteur)]
    for i in range(hauteur):
        if i == 0 or i == hauteur-1:
            # Création des murs du haut et du bas
            laby[i] = [1 for _ in range(largeur)]
        else:
            if i % 2 == 0:
                laby[i].append(1)
                # Génération de passages aléatoires entre murs de croisement
                for j in range(largeur-2):
                    if j % 2 == 0:
                        num = rd.randint(0, 9)
                        if num < 7:
                            laby[i].append(0)
                        else:
                            laby[i].append(1)
                    else:
                        laby[i].append(1)
                laby[i].append(1)
            else:
                # Génération de passages aléatoires entre murs de croisement
                laby[i].append(1)
                for k in range(largeur-2):
                    if k % 2 == 1:
                        num = rd.randint(0, 9)
                        if num < 7:
                            laby[i].append(0)
                        else:
                            laby[i].append(1)
                    else:
                        laby[i].append(0)
                laby[i].append(1)
    return laby


def passagePossible(dicoJeu, i, j):
    '''
    Renvoie True si le passage dans la case donnée est possible, False sinon.
    '''
    laby = dicoJeu["laby"]

    if i > len(laby[0]) - 1 or i < 0 or j > len(laby) - 1 or j < 0:
        return False
    return laby[j][i] != 1  # Si la case n'est pas un mur


def typeCellule(dicoJeu, i, j):
    '''
    Renvoie le type de la cellule donnée (mur, entree, sortie, impasse, passage, carrefour).
    ---
    i, j: Coordonnées de la cellule
    '''
    laby = dicoJeu["laby"]
    entree = dicoJeu["entree"]
    sortie = dicoJeu["sortie"]

    if [j, i] == entree:
        return "entree"
    elif [j, i] == sortie:
        return "sortie"
    elif laby[j][i] == 1:
        return "mur"
    else:
        # On compte le nombre de murs autour de la cellule
        voisins = [passagePossible(dicoJeu, i-1, j), passagePossible(dicoJeu, i+1, j),
                   passagePossible(dicoJeu, i, j-1), passagePossible(dicoJeu, i, j+1)]
        if voisins.count(False) == 3:
            return "impasse"
        elif voisins.count(False) == 2:
            return "passage"
        else:
            return "carrefour"


def tracerCarré(couleur, x=None, y=None):
    '''
    Trace un carré de la couleur donnée.
    ---
    couleur: couleur du carré
    x, y: coordonnées du coin inférieur gauche du carré
    '''
    if x != None and y != None:
        t.goto(x, y)
    # On dessine un carré
    t.color(couleur)
    t.fillcolor(couleur)
    t.begin_fill()
    for _ in range(4):
        t.forward(50)
        t.left(90)
    t.end_fill()


def testClick(x, y):
    '''
    Renvoie des informations sur la case cliquée. (débug)
    ---
    x, y: coordonnées du clic
    '''
    laby = dicoJeu["laby"]
    x_spawn, y_spawn = dicoJeu["spawn"]
    taille_mur = dicoJeu["taille_mur"]

    longueur_laby = len(laby[0])
    hauteur_laby = len(laby)

    # On vérifie que le clic est dans le labyrinthe
    if x < x_spawn or x > x_spawn + taille_mur * longueur_laby or y < y_spawn or y > y_spawn + taille_mur * hauteur_laby:
        print("Vous avez cliqué en dehors du labyrinthe")
    else:
        # On renvoie les infos sur la case cliquée
        case = pixel2cell(dicoJeu, x, y)
        print("Vous avez cliqué sur la case de coordonnées x =",
              case[0], "y =", case[1])
        cos = cell2pixel(dicoJeu, case[0], case[1])
        print("Son centre est aux coordonnées x =", cos[0], "y =", cos[1])
        print("Type de la cellule :", typeCellule(dicoJeu, case[0], case[1]))


def pixel2cell(dicoJeu, x_t, y_t):
    '''
    Renvoie les numéros de grille de la case cliquée.
    ---
    x_t, y_t: coordonnées du clic
    '''
    x_spawn, y_spawn = dicoJeu["spawn"]
    taille_mur = dicoJeu["taille_mur"]

    # Formule pour trouver la case cliquée
    cel_x = (round(x_t) - x_spawn) // taille_mur
    cel_y = (round(y_t) - y_spawn) // taille_mur

    return cel_x, cel_y


def cell2pixel(dicoJeu, i, j):
    '''
    Renvoie les coordonnées du centre de la case indiquée.
    ---
    i, j: numéro de grille de la case
    '''
    x_spawn, y_spawn = dicoJeu["spawn"]
    taille_mur = dicoJeu["taille_mur"]

    # Formule pour trouver le centre de la case
    x_pixel = x_spawn + taille_mur * i + taille_mur // 2
    y_pixel = y_spawn + taille_mur * j + taille_mur // 2

    return x_pixel, y_pixel


def bas():
    '''
    Déplace la tortue d'une case vers le bas.
    '''
    global chemin_parcouru

    cell = pixel2cell(dicoJeu, t.xcor(), t.ycor())
    next_cell = (cell[0], cell[1] + 1)

    # On vérifie que le déplacement est possible
    if passagePossible(dicoJeu, next_cell[0], next_cell[1]):
        t.setheading(90)
        t.forward(50)
        # On ajoute le déplacement à la liste du chemin parcouru
        chemin_parcouru.append("b")
    # On change la couleur de la tortue en fonction de son emplacement
    updateTurtle(dicoJeu, next_cell)


def haut():
    '''
    Déplace la tortue d'une case vers le haut.
    '''
    global chemin_parcouru

    cell = pixel2cell(dicoJeu, t.xcor(), t.ycor())
    next_cell = (cell[0], cell[1] - 1)

    # On vérifie que le déplacement est possible
    if passagePossible(dicoJeu, next_cell[0], next_cell[1]):
        t.setheading(-90)
        t.forward(50)
        # On ajoute le déplacement à la liste du chemin parcouru
        chemin_parcouru.append("h")
    # On change la couleur de la tortue en fonction de son emplacement
    updateTurtle(dicoJeu, next_cell)


def gauche():
    '''
    Déplace la tortue d'une case vers la gauche.
    '''
    global chemin_parcouru

    cell = pixel2cell(dicoJeu, t.xcor(), t.ycor())
    next_cell = (cell[0] - 1, cell[1])

    # On vérifie que le déplacement est possible
    if passagePossible(dicoJeu, next_cell[0], next_cell[1]):
        t.setheading(-180)
        t.forward(50)
        # On ajoute le déplacement à la liste du chemin parcouru
        chemin_parcouru.append("g")
    # On change la couleur de la tortue en fonction de son emplacement
    updateTurtle(dicoJeu, next_cell)


def droite():
    '''
    Déplace la tortue d'une case vers la droite.
    '''
    global chemin_parcouru

    cell = pixel2cell(dicoJeu, t.xcor(), t.ycor())
    next_cell = (cell[0] + 1, cell[1])

    # On vérifie que le déplacement est possible
    if passagePossible(dicoJeu, next_cell[0], next_cell[1]):
        t.setheading(0)
        t.forward(50)
        # On ajoute le déplacement à la liste du chemin parcouru
        chemin_parcouru.append("d")
    # On change la couleur de la tortue en fonction de son emplacement
    updateTurtle(dicoJeu, next_cell)


def victoire(dicoJeu):
    '''
    Fonction de victoire : affiche un message de victoire et le temps de résolution.
    ---
    dicoJeu: dictionnaire du jeu
    '''
    global chemin_parcouru

    # On enregistre le temps de résolution
    dicoJeu["arrivee"] = tm.time()

    t.color("lime")
    t.update()
    t.hideturtle()
    t.up()
    t.forward(40)
    t.down()
    t.write("Victoire !", font=("Arial", 20, "normal"))
    t.up()
    t.left(90)
    t.forward(20)
    t.down()
    t.write("Temps de résolution: " +
            str(round(dicoJeu["arrivee"] - dicoJeu["depart"])) + "s", font=("Arial", 16, "normal"))
    t.update()

    # On affiche le chemin gagnant
    entree_x, entree_y = cell2pixel(
        dicoJeu, dicoJeu['entree'][1], dicoJeu['entree'][0])
    t.up()
    t.hideturtle()
    t.goto(entree_x, entree_y)
    t.showturtle()
    t.down()
    t.pensize(3)
    t.color("cyan")
    t.title("Labyrinthe - Victoire : visualisation du chemin gagnant")

    dicoJeu["running"] = False
    t.tracer(1)
    t.hideturtle()
    if dicoJeu["mode"] == "auto":
        # Ajout de la sortie dans le chemin gagnant
        case_x, case_y = dicoJeu["sortie"][1], dicoJeu["sortie"][0]
        chemin.append((case_x, case_y))
        # Simplification du chemin
        chem = simplifierChemin(chemin)
        suivreCheminCos(chem)
    else:
        # Affichage du chemin parcouru
        chem = chemin_parcouru.copy()
        suivreCheminDir(chem)
    t.update()

    # Fin de la partie
    t.title("Labyrinthe - Partie terminée (cliquez pour fermer)")
    t.exitonclick()


def simplifierChemin(chemin):
    '''
    Supprime les allers-retours inutiles dans le chemin.
    ---
    chemin : chemin à simplifier (en liste de tuples)
    '''
    for tu in chemin:
        if chemin.count(tu) > 1:
            fi = chemin.index(tu)
            li = len(chemin) - 1 - chemin[::-1].index(tu)
            for _ in range(fi, li):
                chemin.pop(fi+1)
    return chemin


def suivreCheminCos(chemin):
    '''
    Parcours le chemin en utilisant les coordonnées
    ---
    chemin : chemin à suivre (en liste de tuples)
    '''
    for coord in chemin:
        x, y = cell2pixel(dicoJeu, coord[0], coord[1])
        t.goto(x, y)


def suivreCheminDir(chemin):
    '''
    Parcours le chemin en utilisant les directions
    ---
    chemin : chemin à suivre (en liste de directions)
    '''
    for v in chemin:
        if v == "g":
            gauche()
        elif v == "d":
            droite()
        elif v == "h":
            haut()
        elif v == "b":
            bas()


def inverserChemin(chemin):
    '''
    Invrse le chemin
    ---
    chemin : chemin à inverser (en liste de directions)
    '''
    chemin = chemin[::-1]
    for v in chemin:
        if v == "g":
            droite()
        elif v == "d":
            gauche()
        elif v == "h":
            bas()
        elif v == "b":
            haut()


def updateTurtle(dicoJeu, next_cell):
    '''
    Met à jour la couleur de la tortue en fonction de son emplacement.
    ---
    dicoJeu : dictionnaire du jeu
    next_cell : coordonnées de la prochaine case
    '''
    if dicoJeu["running"]:
        type_next = typeCellule(dicoJeu, next_cell[0], next_cell[1])
        if type_next == "sortie":
            victoire(dicoJeu)
        elif type_next == "impasse":
            t.color("pink")
        elif type_next == "carrefour":
            t.color("purple")
        elif type_next == "mur":
            t.color("red")
            print("Erreur, mur infranchissable")
        else:
            t.color("black")
    else:
        t.color("cyan")


def prochaineCase(case_x, case_y, i):
    '''
    Renvoie les coordonnées de la case voisine en fonction de l'index.
    '''
    if i == 0:
        return case_x, case_y-1
    elif i == 1:
        return case_x+1, case_y
    elif i == 2:
        return case_x, case_y+1
    else:
        return case_x-1, case_y


def explorer():
    '''
    Explore le labirynthe actuel à la recherche de la sortie.
    '''
    case_x, case_y = pixel2cell(dicoJeu, t.xcor(), t.ycor())
    while typeCellule(dicoJeu, case_x, case_y) != "sortie" and dicoJeu["running"]:
        case_x, case_y = pixel2cell(dicoJeu, t.xcor(), t.ycor())
        # Sélection du voisin
        case = grille[case_x][case_y]
        for i in range(4):
            if case[i] == False:
                new_case_x, new_case_y = prochaineCase(case_x, case_y, i)
                if len(chemin) > 1:
                    if chemin[-2][0] == new_case_x and chemin[-2][1] == new_case_y:
                        continue
                grille[case_x][case_y][i] = True
                if passagePossible(dicoJeu, new_case_x, new_case_y) == False:
                    continue
                if i == 0:
                    haut()
                elif i == 1:
                    droite()
                elif i == 2:
                    bas()
                else:
                    gauche()
                case_x, case_y = pixel2cell(dicoJeu, t.xcor(), t.ycor())
                chemin.append((case_x, case_y))
                break
        else:
            try:
                case_prec = chemin[-2]
            except IndexError:
                print(
                    "Erreur, résolution impossible, je me suis perdue dans le labyrinthe...")
                t.clear()
                t.hideturtle()
                t.done()
                t.exitonclick()
                break
            if case_x < case_prec[0]:
                droite()
            elif case_x > case_prec[0]:
                gauche()
            elif case_y > case_prec[1]:
                haut()
            else:
                bas()
            chemin.pop()
        #tm.sleep(0.3) # A rajouter pour rendre l'exploration plus lente


# FONCTIONS DE L'INTERFACE GRAPHIQUE - TKINTER
def askForParameters(screen):
    '''
    Demande à l'utilisateur, avec une interface graphique, les paramètres du jeu (mode de résolution et de génération du labyrinthe)
    ---
    screen: turtle.Screen
    '''
    result = []
    canvas = screen.getcanvas()

    # Mode de résolution
    # Création des boutons
    b1 = Button(canvas.master, text="Résolution manuelle",
                command=lambda: result.append("manual"))
    b1.pack(padx=10, pady=10, side=LEFT)

    b2 = Button(canvas.master, text="Résolution automatique",
                command=lambda: result.append("auto"))
    b2.pack(padx=10, pady=10, side=RIGHT)

    title = Label(
        canvas.master, text="Sélectionnez votre mode de jeu", justify=CENTER)
    title.pack()

    # Boucle d'attente
    while len(result) == 0:
        screen.update()

    # Destruction des boutons
    b1.destroy()
    b2.destroy()
    title.destroy()

    # Mode de génération
    # Création des boutons
    b1 = Button(canvas.master, text="Sélection d'un labyrithe déjà généré",
                command=lambda: result.append("manual"), width=25,)
    b1.pack(padx=10, pady=10, side=LEFT)

    b2 = Button(canvas.master, text="Génération aléatoire",
                command=lambda: result.append("random"), width=25)
    b2.pack(padx=10, pady=10, side=RIGHT)

    title = Label(
        canvas.master, text="Sélectionnez votre type de labyrinthe", justify=CENTER)
    title.pack()

    # Boucle d'attente
    while len(result) == 1:
        screen.update()

    # Destruction des boutons
    b1.destroy()
    b2.destroy()
    title.destroy()

    # Enregistrement des résultats
    dicoJeu["mode"] = result[0]
    dicoJeu["generation"] = result[1]


def askLaby(screen):
    '''
    Permet à l'utilisateur de choisir un labyrinthe parmi ceux présents dans le dossier labys
    ---
    screen: turtle.Screen
    '''
    global grille
    labys = []
    canvas = screen.getcanvas()
    confirm = []

    # Destruction des boutons
    screen.title("Labyrinthe - Sélectionnez un labyrinthe (dossier labys)")
    # Création des boutons
    confirmer = Button(canvas.master, text="Confirmer",
                       command=lambda: confirm.append(1), justify=RIGHT)
    confirmer.pack(pady=10, padx=10, side=RIGHT)

    # Récupération des fichiers
    files = [f for f in listdir("labys") if isfile(join("labys", f))]
    files.sort()

    # Création des boutons
    buttons = []
    for i in range(len(files)):
        b = Button(canvas.master, text=files[i], command=lambda i=i: [
                   labys.append(files[i]), afficheGraphique(dicoJeu, fichier=files[i])])
        b.pack(padx=10, pady=10, side=LEFT)
        buttons.append(b)

    # Boucle d'attente
    while len(confirm) == 0:
        screen.update()

    # Destruction des boutons
    confirmer.destroy()
    for v in buttons:
        v.destroy()

    # Enregistrement des résultats
    fichier = labyFromFile(labys[-1])
    dicoJeu["laby"] = fichier[0]
    dicoJeu["entree"] = fichier[1]
    dicoJeu["sortie"] = fichier[2]
    grille = [[[False, False, False, False]
               for j in range(len(fichier[0]))] for i in range(len(fichier[0][0]))]


def tryRandomLaby(screen):
    '''
    Affiche un labyrinthe aléatoire et demande à l'utilisateur s'il veut le garder ou en générer un autre
    ---
    screen: turtle.Screen
    '''
    canvas = screen.getcanvas()
    confirm = []

    screen.title("Labyrinthe - Choisissez un labyrinthe")

    # Générer et enregistrer un nouveau labyrinthe
    def new_laby():
        global grille
        laby = genererLabyAleatoire()
        entree = dicoJeu["entree"]
        sortie = dicoJeu["sortie"]
        laby[entree[0]][entree[1]] = 0
        laby[sortie[0]][sortie[1]] = 0
        dicoJeu["laby"] = laby
        grille = [[[False, False, False, False]
                   for j in range(len(laby))] for i in range(len(laby[0]))]
        afficheGraphique(dicoJeu)

    # Création des boutons
    generer = Button(canvas.master, text="Générer un autre",
                     command=new_laby, justify=CENTER)
    generer.pack(padx=10, pady=10, side=LEFT)

    confirmer = Button(canvas.master, text="Confirmer",
                       command=lambda: confirm.append(1), justify=CENTER)
    confirmer.pack(padx=10, pady=10, side=RIGHT)

    # Enregistrement des résultats
    dicoJeu["entree"] = [9, 0]
    dicoJeu["sortie"] = [1, 16]
    new_laby()

    # Boucle d'attente
    while len(confirm) == 0:
        screen.update()

    # Destruction des boutons
    generer.destroy()
    confirmer.destroy()


# Paramètres du jeu
askForParameters(screen)

laby = None
# Génération du labyrinthe
if dicoJeu["generation"] == "manual":
    laby = askLaby(screen)
else:
    laby = tryRandomLaby(screen)

# Debug
if dicoJeu["debug"]:
    # t.tracer(0)
    t.onscreenclick(testClick)
    print("Debug mode: ON")
    t.listen()

# Lancement de la partie
dicoJeu["running"] = True
entree_x, entree_y = cell2pixel(
    dicoJeu, dicoJeu['entree'][1], dicoJeu['entree'][0])
t.goto(entree_x, entree_y)
t.showturtle()
t.speed('fastest')
t.color('black')
screen.title("Labyrinthe - Partie en cours")

# Déplacement manuel
if dicoJeu["mode"] == "manual":
    t.onkeypress(gauche, "Left")
    t.onkeypress(droite, "Right")
    t.onkeypress(haut, "Up")
    t.onkeypress(bas, "Down")
    t.listen()
    dicoJeu["depart"] = tm.time()

# Déplacement automatique
else:
    dicoJeu["depart"] = tm.time()
    explorer()

t.mainloop()
