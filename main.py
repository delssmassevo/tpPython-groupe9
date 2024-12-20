import tkinter  as tk
from tkinter import messagebox,ttk
import mysql.connector
import csv

class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x720")
        self.title("Gestion Des Bourses D'Etudes")
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')
        self.style = ttk.Style(self)
        self.style.theme_use('alt')
        self.style.configure('TNotebook.Tab',background='skyblue', font=('Arial',13,'bold'), padding=8)

        self.bourse = tk.Frame(self.notebook)
        self.evaluation = tk.Frame(self.notebook)
        self.liste_candidat = tk.Frame(self.notebook)
        self.notebook.add(self.bourse, text='Bourse')
        self.notebook.add(self.evaluation, text='Evaluation')
        self.notebook.add(self.liste_candidat, text='Liste de tout les candidats')

        #Initialisation des variables bourses
        self.nom_bourse = tk.StringVar()
        self.description = tk.StringVar()
        self.date = tk.StringVar()
        self.montant = tk.IntVar() 
        #Initialisation des variables evaluations
        self.candidats = tk.StringVar()

        self.set_bourse()
        self.connexion_db()
        self.tableau_bourse()
        self.tableau_cand_save()
        self.tableau_liste_candidats()
        self.set_evaluation()

    def set_bourse(self):
        labels = ["Nom bourse","Montant","Description","Date"]
        variables = [self.nom_bourse, self.montant, self.description, self.date]
        for i, var in enumerate(variables):
            tk.Label(self.bourse, text=f'{labels[i]} :', font=('Arial',12,'bold')).grid(row=i+1, column=0, padx=20, pady=5, sticky='w')
            self.entrees = tk.Entry(self.bourse, textvariable= var, width=50, bd=3, font=('Arial',12))
            self.entrees.grid(row=i+1, column=1, pady=5,padx=20)
        ajout_bourse = tk.Button(self.bourse, text='Ajouter la bourse',bg='skyblue', font=('Arial',13,'bold'),width=30, command= self.ajoutBourse)
        ajout_bourse.grid(row=5, column=1, pady=5, padx=20)

        


    def set_evaluation(self):
        eval_btn = tk.Button(self.evaluation, text='Evaluer le candidat',bg='skyblue', font=('Arial',13,'bold'),width=30, command=self.evaluer)
        eval_btn.grid(row=3, column=0, pady=5, padx=20)

    def tableau_cand_save(self):
        """====== CREATION DE LA TABLE LISTE DE CANDIDAT APTENT A OBTENIR UNE BOURSE"""
        texte = tk.Label(self.evaluation, text="Listes des candidats evaluer", font=('Arial', 12,'bold italic'))
        texte.grid(row=8, column=0, columnspan=4, pady=10)
        
        heads = ['Id','Nom','Email','Téléphone','Note academique','Bourse']
        self.table_evaluation =ttk.Treeview(self.evaluation, columns=[i for i in heads], show='headings')
        self.table_evaluation.grid(row=9, column=0, columnspan=4, padx=20, pady=10, sticky="nsew")

        for head in heads:
            if head == 'Id':
                self.table_evaluation.heading(head, text=head)
                self.table_evaluation.column(head, width=70)
            else:
                self.table_evaluation.heading(head, text=head)
                self.table_evaluation.column(head, width=190)
    def evaluer(self):
        try:
            conn = mysql.connector.connect(
                host = 'localhost',
                user = 'root',
                database = 'gestionbourse'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT id,nom,email,tel,note_academique,bourse FROM candidats WHERE note_academique>=60")
            with open('candidat_evaluer.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(cursor.fetchall())

            for item in self.table_list_candidats.get_children():
                self.table_list_candidats.delete(item)
            with open('candidat_evaluer.csv', 'r') as csvfile:
                lecteur = csv.reader(csvfile)
                for row in lecteur:
                    self.table_evaluation.insert('', 'end', values=row)

        except mysql.connector.Error as err:
            messagebox.showerror('Erreur', "Probleme lors du chargement des candidats")

    def tableau_liste_candidats(self):  

        """===== CREATION DE LA TABLE LISTE DES CANDIDATS"""
        texte = tk.Label(self.liste_candidat, text="Listes de tout les candidats", font=('Arial', 12,'bold italic'))
        texte.grid(row=0, column=0, columnspan=4, pady=10)
        
        heads = ['Id','Nom','sexe','Email','Téléphone','Note academique','Bourse','motivation']
        self.table_list_candidats =ttk.Treeview(self.liste_candidat, columns=[i for i in heads], show='headings')
        self.table_list_candidats.grid(row=1, column=0, columnspan=4, padx=20, pady=10, sticky="nsew")

        for head in heads:
            if head == 'Id':
                self.table_list_candidats.heading(head, text=head)
                self.table_list_candidats.column(head, width=70)
            else:
                self.table_list_candidats.heading(head, text=head)
                self.table_list_candidats.column(head, width=150)
        try:
            conn = mysql.connector.connect(
                host = 'localhost',
                user = 'root',
                database = 'gestionbourse'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM candidats")
            results = cursor.fetchall()
            for item in self.table_list_candidats.get_children():
                self.table_list_candidats.delete(item)
            data_cand = []
            for row in results:
                self.table_list_candidats.insert("", tk.END, values=row)
                data_cand.append(row[1])
            self.cand = [i for i in data_cand]
        except mysql.connector.Error as err:
            messagebox.showerror('Erreur', "Probleme lors du chargement des candidats")
            
    def tableau_bourse(self):
        """====== CREATION DE LA TABLE LISTE DE BOURSE"""
        texte = tk.Label(self.bourse, text="Listes des bourse disponible", font=('Arial', 12,'bold italic'))
        texte.grid(row=6, column=0, columnspan=4, pady=10)
        
        heads = ['Id','Nom de la bourse','Montant','Description','Date']
        self.table_bourse =ttk.Treeview(self.bourse, columns=[i for i in heads], show='headings')
        self.table_bourse.grid(row=7, column=0, columnspan=4, padx=20, pady=10, sticky="nsew")

        for head in heads:
            if head == 'Id':
                self.table_bourse.heading(head, text=head)
                self.table_bourse.column(head, width=80)
            else:
                self.table_bourse.heading(head, text=head)
                self.table_bourse.column(head, width=250)
        try:
            conn = mysql.connector.connect(
                host = 'localhost',
                user = 'root',
                database = 'gestionbourse'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM bourses")
            results = cursor.fetchall()
            for item in self.table_bourse.get_children():
                self.table_bourse.delete(item)
            for row in results:
                self.table_bourse.insert("", tk.END, values=row)

        except mysql.connector.Error as err:
            messagebox.showerror('Erreur', "Probleme lors du chargement de bourse")

    def connexion_db(self):
        try:
            conn = mysql.connector.connect(
                host = 'localhost',
                user = 'root',
            )
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS gestionbourse")
            conn.database = "gestionbourse"
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS bourses(
            id INT AUTO_INCREMENT PRIMARY KEY,
            nom_bourse VARCHAR(150),
            montant INT(11),
            description TEXT,
            date DATE
            )
            """)
            conn.commit()
        except mysql.connector.Error as err:
            print(f'Erreur : {err}')
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def ajoutBourse(self):
        #Ajouter les information introduit par l'utilisateur dans la base de donneés
        nom = self.nom_bourse.get()
        montant = self.montant.get()
        description = self.description.get()
        date = self.date.get()
        if nom !="" and montant != "" and description != "" and date != "":
            try:
                conn = mysql.connector.connect(
                    host = 'localhost',
                    user = 'root',
                    database = 'gestionbourse'
                )
                cursor = conn.cursor()
                sq = "INSERT INTO bourses(nom_bourse,montant,description,date) VALUES(%s,%s,%s,%s)"
                val = (nom,montant,description,date)
                cursor.execute(sq, val)
            except mysql.connector.Error as err:
                print(f'Erreur : {err}')
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
        else:
            messagebox.showerror("Erreur","Veillez remplir tout le formulaire")





if __name__ == '__main__' :
    app = Root()
    app.mainloop()