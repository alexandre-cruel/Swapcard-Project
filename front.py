from tkinter import *


def Affichage_Profil1():
    Texte.set('Profil 1 \n blabla \n blabla')
    recom = 1

def Affichage_Profil2():
    Texte.set('Profil 2 \n blabla \n blabla')
    recom = 2

def Affichage_Profil3():
    Texte.set('Profil 3 \n blabla \n blabla')
    recom = 3

def Affichage_Profil4():
    Texte.set('Profil 4 \n blabla \n blabla')
    recom = 4

def Affichage_Profil5():
    Texte.set('Profil 5 \n blabla \n blabla')
    recom = 5

def Affichage_Profil6():
    Texte.set('Profil 6 \n blabla \n blabla')
    recom = 6

def Recommand():
    if recom == 1:
        Texte_retour.set('la recommandation du profil 1 est \n blabla')
    elif recom == 2:
        Texte_retour.set('la recommandation du profil 2 est \n blabla')
    elif recom == 3:
        Texte_retour.set('la recommandation du profil 3 est \n blabla')
    elif recom == 4:
        Texte_retour.set('la recommandation du profil 4 est \n blabla')
    elif recom == 5:
        Texte_retour.set('la recommandation du profil 5 est \n blabla')
    elif recom == 6:
        Texte_retour.set('la recommandation du profil 6 est \n blabla')



window = Tk()
window.title('Recommendation Swapcard')
window.geometry('700x500+400+400')

recom = 0

Frame_bouton = Frame(window,borderwidth=3)
Frame_bouton.pack(side=TOP, padx=10, pady=10)

Bouton1 = Button(Frame_bouton, text='Profil 1', command=Affichage_Profil1)
Bouton1.pack(side=LEFT, padx=10, pady=10)

Bouton2 = Button(Frame_bouton, text='Profil 2', command=Affichage_Profil2)
Bouton2.pack(side=LEFT, padx=10, pady=10)

Bouton3 = Button(Frame_bouton, text='Profil 3', command=Affichage_Profil3)
Bouton3.pack(side=LEFT, padx=10, pady=10)

Bouton4 = Button(Frame_bouton, text='Profil 4', command=Affichage_Profil4)
Bouton4.pack(side=LEFT, padx=10, pady=10)

Bouton5 = Button(Frame_bouton, text='Profil 5', command=Affichage_Profil5)
Bouton5.pack(side=LEFT, padx=10, pady=10)

Bouton6 = Button(Frame_bouton, text='Profil 6', command=Affichage_Profil6)
Bouton6.pack(side=LEFT, padx=10, pady=10)

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

Bouton_retour = Button(Frame_retour, text='Recommander', command=Recommand)
Bouton_retour.pack(side=TOP, padx=10, pady=10)

Label_retour = Label(Frame_retour, textvariable=Texte_retour)
Label_retour.pack(side=TOP, padx=10, pady=10)

window.mainloop()