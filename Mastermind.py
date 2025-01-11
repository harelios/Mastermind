import random
from tkinter import * 
from tkinter import ttk,END
from tkinter.messagebox import *
from time import sleep
import tkinter as tk 

root = Tk()
entry = ttk.Entry(root)
entry.pack() #Permet de mettre un input dans la page
text_area = Text(root,height=20,width=120)
text_area.pack()

valeur = StringVar()
valeur.set("")
entree = Entry(root,textvariable=valeur,width=30)
entree.pack()



def generer_code(couleur, longueur=4):
    return [random.choice(couleur) for _ in range(longueur)]

def evaluer_proposition(proposition, code_secret):
    resultat = []
    
    code_secret_copie = code_secret[:]
    marque = [False] * len(code_secret)
    
    #Pour les boules noires
    for i, (p,c) in enumerate(zip(proposition, code_secret_copie)):
        if p == c:
            resultat.append("noirs")
            marque[i] = True
            code_secret_copie[i] = None
        else:
            resultat.append("None")
    #Pour les boules blanches
    for i, p in enumerate(zip(proposition)):
        if resultat[i] == None and p in code_secret_copie:
            resultat[i] = "blanc"
            code_secret_copie[code_secret_copie.index(p)] = None
        elif resultat[i] == None:
            resultat[i] = "aucun"
    
    return resultat

            
            
def afficher_resultat(bulles_noires, bulles_blanches):
    text_area.insert(END,f"Bien placées (bulles_noires) :{bulles_noires}")
    text_area.insert(END,f"Mal placées (bulles blanches) :{bulles_blanches}")
    
def recupere():
    return valeur.get()  
couleur = ["rouge","jaune","vert","bleu","violet","rose","beige"]
longueur_code = 4
tentative_max = 10
tentative_actuelle = 0
    
text_area.insert(END,f"Bienvenue dans le jeu du Mastermind !!! \n Vous devez deviner la bonne combinaison de 4 couleurs choisi aléatoirement.\n Les couleurs possibles sont : {couleur}.")

code_secret = generer_code(couleur, longueur_code)


def afficher_boule_avec_ordre(canvas,resultat,x_depart = 10, y_depart = 10, taille=20, espace=5):
    
    #:param canvas: Le widget tkinter.Canvas où afficher les boules.
    #:param noirs: Le nombre de boules noires à afficher.
    #:param blancs: Le nombre de boules blanches à afficher.
    #:param x_depart: Position x initiale.
    #:param y_depart: Position y initiale.
    #:param taille: Diamètre des boules.
    #:param espace: Espace entre chaque boule.
    
    canvas.delete("all")
    x = x_depart
    for etat in resultat:
        if etat == "noirs":
            canvas.create_oval(x,y_depart, x + taille, y_depart + taille, fill="black", outline="black")
        elif etat == "blanc":
            canvas.create_oval(x,y_depart, x + taille, y_depart + taille, fill="white", outline="white")
        x+=taille + espace

def valider_tentatives():
    global tentative_actuelle
    if tentative_actuelle >=tentative_max:
        text_area.insert(END,f"Vous n'avez plus de tentatives ! le code secret était : {code_secret}")
        return
        

    proposition = recupere().strip().split() #Transforme le texte en liste de couleurs
    valeur.set("")
    if len(proposition) != longueur_code or any(c not in couleur for c in proposition):
        text_area.insert(END,"Entrez le bon nombre de couleurs parmis celle disponible ! \n")
        
        
    resultat = evaluer_proposition(proposition,code_secret)
    
    text_area.insert(END,f"{tentative_actuelle + 1} / {tentative_max} : {proposition}")

    afficher_boule_avec_ordre(canvas_boules,resultat)

    if resultat.count("noirs") == longueur_code:
        text_area.insert(END," Victoire !!!") 
        return

    tentative_actuelle += 1
    if tentative_actuelle == tentative_max:
        text_area.insert(END,f"Tentatives terminées ! Le code secret était : {code_secret}")
   
canvas_boules = tk.Canvas(root,width=300, height=50, bg="lightgray")
canvas_boules.pack()
    
bouton = Button(root,text="Entrer",command=valider_tentatives)
bouton.pack()
        
root.title("Mastermind")
root.geometry("100x100") #Taille de la fenêtre
ttk.Label(root,text="Boules Noirs = bon\nBoules Blanches = Pas bon").pack()

root.mainloop()