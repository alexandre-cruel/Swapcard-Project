# -*- coding: utf-8 -*-
from tkinter import *
import main


def Affichage_Profil1():
    Texte.set('Profil 1 \nPROFESSION: Ingénieur\n')
    Wentree.forget()
    global recom
    recom = 1


def Affichage_Profil2():
    Texte.set('Profil 2 \nPROFESSION: Cadre\n ')
    Wentree.forget()
    global recom
    recom = 2


def Affichage_Profil3():
    Texte.set('Profil 3 \nPROFESSION: \n')
    Wentree.pack(padx=10, pady=10)
    global recom
    recom = 3


def Recommand():
    if recom == 1:
        Texte_retour.set('Recommandation en cours, veuillez patienter ...')
        reponse = main.recommendation('Ingénieur')
        Texte_retour.set('la recommandation du profil 1 est \n' + reponse)
    elif recom == 2:
        Texte_retour.set('Recommandation en cours, veuillez patienter ...')
        reponse = main.recommendation('Cadre')
        Texte_retour.set('la recommandation du profil 2 est \n' + reponse)
    elif recom == 3:
        Texte_retour.set('Recommandation en cours, veuillez patienter ...')
        reponse = main.recommendation(entree)
        Texte_retour.set('la recommandation du profil 3 est \n' + reponse)


window = Tk()
window.title('Recommendation Swapcard')
window.geometry('700x500+400+400')

recom = 0

Frame_bouton = Frame(window,borderwidth=3)
Frame_bouton.pack(side=TOP, padx=10, pady=10)

entree = StringVar()
entree.set("Entrée un métier")

Wentree= Entry(window, textvariable=entree)

Bouton1 = Button(Frame_bouton, text='Profil 1', command=Affichage_Profil1)
Bouton1.pack(side=LEFT, padx=10, pady=10)

Bouton2 = Button(Frame_bouton, text='Profil 2', command=Affichage_Profil2)
Bouton2.pack(side=LEFT, padx=10, pady=10)

Bouton3 = Button(Frame_bouton, text='Profil 3', command=Affichage_Profil3)
Bouton3.pack(side=LEFT, padx=10, pady=10)

Frame_texte = Frame(window, borderwidth=3)
Frame_texte.pack(side=TOP, padx=10, pady=10)

Texte = StringVar()
Texte.set('')

Label_texte = Label(Frame_texte, textvariable=Texte)
Label_texte.pack(side=TOP, padx=10, pady=10)

Texte_retour = StringVar()
Texte_retour.set('')


Frame_retour = Frame(window, borderwidth=3)
Frame_retour.pack(side=BOTTOM, padx=10, pady=10)

Label_retour = Label(Frame_retour, textvariable=Texte_retour)
Label_retour.pack(side=TOP, padx=10, pady=10)

Bouton_retour = Button(Frame_retour, text='Recommander', command=Recommand)
Bouton_retour.pack(side=TOP, padx=10, pady=10)



window.mainloop()
