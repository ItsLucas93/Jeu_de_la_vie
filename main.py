import tkinter
from random import randint


class Case:
    def __init__(self, valeur=0):
        self.valeur = valeur

    def estMort(self):
        return self.valeur == 0

    def estVivante(self):
        return self.valeur == 1

    def valeur(self):
        return self.valeur


class Jeu:
    def __init__(self, nblignes=20, nbcolonnes=20):
        self.nblignes = nblignes
        self.nbcolonnes = nbcolonnes
        self.tableau = []
        for i in range(nblignes):
            temp = []
            for j in range(nbcolonnes):
                a = Case()
                temp.append(a)
            self.tableau.append(temp)

    def etapeSuivante(self):
        li_mourrante = []
        li_vivante = []
        for lig in range(self.nblignes):
            for col in range(self.nbcolonnes):
                nb = self.getAdj(lig, col)
                if self.tableau[lig][col].estMort() and nb == 3:
                    li_vivante.append((lig, col))
                elif self.tableau[lig][col].estVivante() and (nb == 2 or nb == 3):
                    li_vivante.append((lig, col))
                else:
                    li_mourrante.append((lig, col))
        for coords in li_mourrante:
            self.tableau[coords[0]][coords[1]].valeur = 0
        for coords in li_vivante:
            self.tableau[coords[0]][coords[1]].valeur = 1

    def getAdj(self, l, c):
        cpt = 0
        for lig in range(-1, 2):
            for col in range(-1, 2):
                if lig != 0 or col != 0:
                    if 0 <= l + lig < self.nblignes and 0 <= c + col < self.nbcolonnes:
                        if self.tableau[l + lig][c + col].estVivante():
                            cpt += 1
        return cpt

    def placeVCelsRandom(self, nb):
        for i in range(self.nblignes):
            for j in range(self.nbcolonnes):
                self.tableau[i][j].valeur = 0
        for i in range(nb):
            lig = randint(0, self.nblignes - 1)
            col = randint(0, self.nbcolonnes - 1)
            while self.tableau[lig][col].estVivante():
                lig = randint(0, self.nblignes - 1)
                col = randint(0, self.nbcolonnes - 1)
            self.tableau[lig][col].valeur = 1

    def grilleEstVide(self):
        for lig in range(self.nblignes):
            for col in range(self.nbcolonnes):
                if self.tableau[lig][col].estVivante():
                    return False
        return True

    def reinit(self):
        self.tableau = []
        for i in range(self.nblignes):
            self.tableau.append([])
            for j in range(self.nbcolonnes):
                self.tableau[i].append(Case())


class Interface:
    def __init__(self, modele):
        self.modele = modele
        self.window_parameter = tkinter.Tk()
        self.window_parameter.title('Paramètres')
        self.window_parameter.iconbitmap('jeudelavie.ico')
        self.window_parameter.configure(background='#A6AAB0')

        tkinter.Label(self.window_parameter, foreground='black', background='white', text="Indiquez le nombre de lignes (max : " + str(self.modele.nblignes) + ")").grid(row=0)
        tkinter.Label(self.window_parameter, foreground='black', background='white', text="Indiquez le nombre de colonnes (max : " + str(self.modele.nbcolonnes) + ")").grid(row=1)
        tkinter.Label(self.window_parameter, foreground='black', background='white', text="Nombre de cases aléatoires").grid(row=2)
        self.e1 = tkinter.Entry(self.window_parameter, foreground='black', background='white', width=3)
        self.e2 = tkinter.Entry(self.window_parameter, foreground='black', background='white', width=3)
        self.e3 = tkinter.Entry(self.window_parameter, foreground='black', background='white', width=6)
        bouton_valider = tkinter.Button(self.window_parameter, text='Valider', foreground='black', background='white', command=lambda: self.validation())
        bouton_valider.grid(row=2, column=2)
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        self.e1.insert(0, 10)
        self.e2.insert(0, 10)
        self.e3.insert(0, 5)
        self.window_parameter.lift()
        self.window_parameter.attributes('-topmost', True)
        self.window_parameter.after_idle(self.window_parameter.attributes, '-topmost', False)
        self.window_parameter.mainloop()

        self.modele.nblignes = self.nblignes
        self.modele.nbcolonnes = self.nbcolonnes
        self.window_main = tkinter.Tk()
        self.window_main.title("Jeu de la vie")
        self.window_main.iconbitmap('jeudelavie.ico')
        self.window_main.configure(background='white')
        self.delai = 1500
        terrain = tkinter.Frame(self.window_main)
        accral = tkinter.Frame(self.window_main)
        accral.configure(background='white')
        cleaquit = tkinter.Frame(self.window_main)
        cleaquit.configure(background='white')
        self.generations = 0
        self.li = []
        for i in range(self.nblignes):
            ligne = []
            for j in range(self.nbcolonnes):
                self.bouton_case = tkinter.Button(terrain, width=2, height=1)
                self.bouton_case.grid(row=i, column=j)
                ligne.append(self.bouton_case)
            self.li.append(ligne)
        self.bouton_start = tkinter.Button(self.window_main, text='Commencer', foreground='black', background='#A6AAB0', command=self.bouton_stop)
        self.bouton_start.pack(side='top', padx=10, pady=5)
        bouton_reset = tkinter.Button(cleaquit, text='    Reset   ', foreground='black', background='#A6AAB0', command=self.ctrl_reinit)
        bouton_reset.pack(side='left', padx=11, pady=5)
        bouton_quitter = tkinter.Button(cleaquit, text='Quitter', foreground='black', background='#A6AAB0', command=self.window_main.destroy)
        bouton_quitter.pack(side='right', padx=20, pady=5)
        self.bouton_accelerer = tkinter.Button(accral, text='Accélérer', foreground='black', background='#A6AAB0', command=self.accelerer)
        self.bouton_accelerer.pack(side='left', padx=10, pady=5)
        self.bouton_ralentir = tkinter.Button(accral, text='Ralentir', foreground='black', background='#A6AAB0', command=self.ralentir)
        self.bouton_ralentir.pack(side='right', padx=20, pady=5)
        accral.pack()
        cleaquit.pack()
        terrain.pack()
        self.lbl_generation = tkinter.Label(self.window_main, text="Génération n°0")
        self.lbl_generation.pack(side='top')
        self.boucle = tkinter.Label(self.window_main, text="")
        self.boucle.pack(side='top')
        self.ctrl_reinit()
        self.window_main.lift()
        self.window_main.attributes('-topmost', True)
        self.window_main.after_idle(self.window_main.attributes, '-topmost', False)
        self.window_main.geometry("1080x720")

    def bouton_stop(self):
        self.bouton_start.config(text='Stop', command=self.bouton_commencer)
        self.pause = False

    def bouton_commencer(self):
        self.bouton_start.config(text='Continue', command=self.bouton_stop)
        self.pause = True

    def accelerer(self):
        self.delai -= (self.delai) / 3
        if self.delai < 2:
            self.delai = 2
            self.bouton_accelerer.configure(text='Max atteint', background='green')
        else:
            self.bouton_accelerer.configure(text='Accélérer', background='#A6AAB0')
            self.bouton_ralentir.configure(text='Ralentir', background='#A6AAB0')

    def validation(self):
        if (0 < int(self.e1.get()) <= self.modele.nblignes) and (0 < int(self.e2.get()) <= self.modele.nbcolonnes) and (
                len(self.e3.get()) <= 1 or 0 <= int(self.e3.get()) <= (int(self.e1.get()) * int(self.e2.get()))):
            self.nblignes = int(self.e1.get())
            self.nbcolonnes = int(self.e2.get())
            if len(self.e3.get()) != 0:
                self.nbaleatoire = int(self.e3.get())
            else:
                self.nbaleatoire = 0
            self.window_parameter.destroy()

    def ralentir(self):
        self.delai += (self.delai) / 3
        if self.delai > 5000:
            self.delai = 5000
            self.bouton_ralentir.configure(text='Min atteint', background='green')
        else:
            self.bouton_ralentir.configure(text='Ralentir', background='#A6AAB0')
            self.bouton_accelerer.configure(text='Accélérer', background='#A6AAB0')

    def replaceIntoAlive(self, i, j):
        self.li[i][j].configure(background='white', command=lambda: self.replaceIntoDead(i, j))
        self.modele.tableau[i][j].valeur = 1

    def replaceIntoDead(self, i, j):
        self.li[i][j].configure(background='black', command=lambda: self.replaceIntoAlive(i, j))
        self.modele.tableau[i][j].valeur = 0

    def formationCase(self, lig, col):
        if self.modele.tableau[lig][col].estVivante():
            self.li[lig][col].config(background='white', command=lambda: self.replaceIntoDead(lig, col))
        if self.modele.tableau[lig][col].estMort():
            self.li[lig][col].config(background='black', command=lambda: self.replaceIntoAlive(lig, col))

    def formationTerrain(self):
        for lig in range(self.nblignes):
            for col in range(self.nbcolonnes):
                self.formationCase(lig, col)

    def finDetectee(self):
        self.boucle.config(text="Partie terminée ! (Cliquez sur \"reset\" pour recommencer.)")
        self.bouton_ralentir.configure(text='Ralentir', background='black')
        self.bouton_accelerer.configure(text='Accélérer', background='black')
        self.bouton_stop()

    def generation(self, nb):
        self.lbl_generation.config(text="Génération n°" + str(nb))

    def ctrl_reinit(self):
        self.bouton_start.config(text='Commencer', command=self.bouton_stop)
        self.pause = True
        self.generations = 0
        self.lbl_generation.configure(text="Génération n°0")
        self.boucle.config(text="")
        self.delai = 1500
        self.modele.reinit()
        self.formationTerrain()


class Controleur:
    def __init__(self, modele):
        self.jeu = modele
        self.interface = Interface(self.jeu)
        self.jeu.placeVCelsRandom(int(self.interface.nbaleatoire))
        self.interface.formationTerrain()
        self.window_main = self.interface.window_main
        self.delai = self.interface.delai
        self.joue()
        self.window_main.mainloop()

    def affiche_generations(self):
        self.interface.generation(self.interface.generations)

    def affichage(self):
        if self.jeu.grilleEstVide():
            self.interface.generations += 1
            self.affiche_generations()
        else:
            self.interface.boucle.config(text="")
            self.interface.generations += 1
            self.affiche_generations()
        self.delai = self.interface.delai
        self.jeu.etapeSuivante()
        self.interface.formationTerrain()
        if self.jeu.grilleEstVide():
            self.interface.formationTerrain()
            self.interface.finDetectee()
            self.interface.generations -= 1

    def joue(self):
        if self.interface.pause == False:
            self.affichage()
        self.window_main.after(int(self.delai), self.joue)


vie = Jeu()
jeu = Controleur(vie)
