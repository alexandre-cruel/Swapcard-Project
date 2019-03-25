# -*- coding: utf-8 -*-
from tkinter import *
import pandas as pd
import main


def Affichage_Profil1():
    Texte.set('Profil 1 \nPROFESSION: Ingénieur\n')
    Wentree.forget()
    global recom
    recom = 1


def Affichage_Profil2():
    Texte.set('Profil 2 \nPROFESSION: CEO\n ')
    Wentree.forget()
    global recom
    recom = 2


def Affichage_Profil3():
    Texte.set('Profil Personnalisé \nPROFESSION: \n')
    Wentree.pack(side=BOTTOM,padx=10, pady=10)
    global recom
    recom = 3

def id_to_label(reponse):
    label = str(reponse.at[0,'user_id'])
    return label

def tag_to_label(reponse):
    label = str(reponse.at[0,'tagsRankingName'])
    return label

def event_to_label(reponse):
    label = str(reponse.at[0,'eventRankingName'])
    return label



def Recommand():
    if recom == 1:
        Texte_retour1.set('Recommandation en cours, veuillez patienter ...')
        reponse = main.recommendation('Ingénieur')
        texte = id_to_label(reponse)
        Texte_retour1.set('Nous recommendons à ce profil les utilisateurs suivants : \n' + texte)
        texte = tag_to_label(reponse)
        Texte_retour2.set('Les domaines susceptibles de vous intéressé sont : \n' + texte)
        texte = event_to_label(reponse)
        Texte_retour3.set('Les evenements susceptibles de vous intéressé sont: \n' + texte)
    elif recom == 2:
        Texte_retour1.set('Recommandation en cours, veuillez patienter ...')
        reponse = main.recommendation('CEO')
        texte = id_to_label(reponse)
        Texte_retour1.set('Nous recommendons à ce profil les utilisateurs suivants : \n' + texte)
        texte = tag_to_label(reponse)
        Texte_retour2.set('Les domaines susceptibles de vous intéressé sont : \n' + texte)
        texte = event_to_label(reponse)
        Texte_retour3.set('Les evenements susceptibles de vous intéressé sont: \n' + texte)
    elif recom == 3:
        Texte_retour1.set('Recommandation en cours, veuillez patienter ...')
        reponse = main.recommendation(entree.get())
        texte = id_to_label(reponse)
        Texte_retour1.set('Nous recommendons à ce profil les utilisateurs suivants : \n' + texte)
        texte = tag_to_label(reponse)
        Texte_retour2.set('Les domaines susceptibles de vous intéressé sont : \n' + texte)
        texte = event_to_label(reponse)
        Texte_retour3.set('Les evenements susceptibles de vous intéressé sont: \n' + texte)

        # table.show()


window = Tk()
window.title('Recommendation Swapcard')
window.geometry('1920x1080')

window.tk.call('wm', 'iconphoto', window._w, PhotoImage(file='esme.png'))
recom = 0



Frame_bouton = Frame(window,borderwidth=3)
Frame_bouton.pack(side=TOP, padx=10, pady=10)


Bouton1 = Button(Frame_bouton, text='Profil 1', command=Affichage_Profil1)
Bouton1.pack(side=LEFT, padx=10, pady=10)

Bouton2 = Button(Frame_bouton, text='Profil 2', command=Affichage_Profil2)
Bouton2.pack(side=LEFT, padx=10, pady=10)

Bouton3 = Button(Frame_bouton, text='Profil Perso', command=Affichage_Profil3)
Bouton3.pack(side=LEFT, padx=10, pady=10)

Frame_texte = Frame(window, borderwidth=3)
Frame_texte.pack(side=TOP, padx=10, pady=10)

entree = StringVar()
entree.set("Entrez un métier")
Wentree= Entry(Frame_texte, textvariable=entree)

Texte = StringVar()
Texte.set('')

Label_texte = Label(Frame_texte, textvariable=Texte)
Label_texte.pack(side=TOP, padx=10, pady=10)


Frame_retour = Frame(window, borderwidth=3)
Frame_retour.pack( padx=10, pady=10)


Texte_retour1 = StringVar()
Texte_retour1.set('')

Label_retour1 = Label(Frame_retour, textvariable=Texte_retour1)
Label_retour1.pack(side=LEFT, padx=10, pady=10)


Texte_retour2 = StringVar()
Texte_retour2.set('')

Label_retour2 = Label(Frame_retour, textvariable=Texte_retour2)
Label_retour2.pack(side=LEFT, padx=10, pady=10)

Texte_retour3 = StringVar()
Texte_retour3.set('')

Label_retour3 = Label(Frame_retour, textvariable=Texte_retour3)
Label_retour3.pack(side=LEFT, padx=10, pady=10)

Bouton_retour = Button(Frame_retour, text='Recommander', command=Recommand)
Bouton_retour.pack(side=TOP, padx=10, pady=10)



window.mainloop()
