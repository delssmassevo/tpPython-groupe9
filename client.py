import tkinter as tk
from tkinter import messagebox,ttk
import mysql.connector

class Fen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x720")
        self.title("Gestion Des Bourses D'Etudes")

        #Initialisation des variables candidatures
        self.bourse = tk.StringVar()
        self.nom = tk.StringVar()
        self.sexe = tk.StringVar()
        self.email = tk.StringVar()
        self.tel = tk.StringVar()
        self.note_academique = tk.IntVar()
        self.motivation = tk.StringVar()

        self.set_bourse_base()
        self.set_candidature()
        self.connexion_db()

    def set_candidature(self):
        labels = ['Selectionner une bourse','Noms du canditat','Sexe','Téléphone du candidats','Email du candidat','Note academique','Motivation du candidat']
        variables = [self.bourse,self.nom,self.sexe,self.tel, self.email, self.note_academique, self.motivation]
        
        tk.Label(self, text="BOURSES D'ETUDES", font=("Arial", 25, 'bold'), fg='blue').grid(row=0, column=1, sticky="w", padx=20, pady=5)
        for i, var in enumerate(variables):
            if labels[i] == 'Selectionner une bourse':
                tk.Label(self, text=f"{labels[i]} :", font=("Arial", 12, 'bold')).grid(row=1, column=0, sticky="w", padx=20, pady=5)
                self.entrees = ttk.Combobox(self,textvariable=self.bourse,width=38, font=("Arial", 13, 'bold'), values=self.dbourse)
                self.entrees.grid(row=1, column=1, pady=5, padx=20)
            elif labels[i] == 'Noms du canditat':
                tk.Label(self, text=f"{labels[i]} :", font=("Arial", 12, 'bold')).grid(row=2, column=0, sticky="w", padx=20, pady=5)
                self.entrees = tk.Entry(self, textvariable= var, width=40, bd=3,font=('Arial',12,'bold'))
                self.entrees.grid(row=2, column=1, pady=5, padx=20)
            elif labels[i] == 'Sexe':
                tk.Label(self, text=f"{labels[i]} :", font=("Arial", 12, 'bold')).grid(row=3, column=0, sticky="w", padx=20, pady=5)
                self.entrees = ttk.Combobox(self,textvariable=self.sexe,width=38, font=("Arial", 13, 'bold'), values=[j for j in ["M","F"]])
                self.entrees.grid(row=3, column=1, pady=5, padx=20)
            else:
                tk.Label(self, text=f"{labels[i]} :", font=("Arial", 12, 'bold')).grid(row=i+3, column=0, sticky="w", padx=20, pady=5)
                self.entrees = tk.Entry(self, textvariable= var, width=40, bd=3,font=('Arial',12,'bold'))
                self.entrees.grid(row=i+3, column=1, pady=5, padx=20)

        save_btn = tk.Button(self, text="S'enregistrer",bg='skyblue', font=('Arial',13,'bold'),width=30, command=self.enregistrement)
        save_btn.grid(row=10, column=1, pady=5,padx=20)
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
            CREATE TABLE IF NOT EXISTS candidats(
            id INT AUTO_INCREMENT PRIMARY KEY,
            nom VARCHAR(100),
            sexe ENUM('M','F'),
            email VARCHAR(100),
            tel VARCHAR(12),
            note_academique INT(3),
            bourse VARCHAR(150),
            motivation TEXT
            )
            """)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS candidataccepter(
            id INT AUTO_INCREMENT PRIMARY KEY,
            nom VARCHAR(100),
            email VARCHAR(100),
            tel VARCHAR(12),
            note_academique INT(3),
            bourse VARCHAR(150)
            )
            """)
        except mysql.connector.Error as err:
            print(f'Erreur : {err}')
        finally:
            if conn.is_connected():
                print("Connexion réussi")
                cursor.close()
                conn.close()
    
    def set_bourse_base(self):
        try:
            conn = mysql.connector.connect(
                host = 'localhost',
                user = 'root',
                database = 'gestionbourse'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM bourses")
            results = cursor.fetchall()
            data_bourse = []
            for row in results:
                data_bourse.append(row[1])
            self.dbourse = [i for i in data_bourse]
        except mysql.connector.Error as err:
            print("Erreur",err)

    def enregistrement(self):
        bourse = self.bourse.get()
        nom = self.nom.get()
        sexe = self.sexe.get()
        email = self.email.get()
        tel = self.tel.get()
        note_academique = self.note_academique.get()
        motivation = self.motivation.get()
        try:
            conn = mysql.connector.connect(
                host = 'localhost',
                user = 'root',
                database = 'gestionbourse'
            )
            cursor = conn.cursor()
            sql = "INSERT INTO candidats(nom,sexe,email,tel,note_academique,bourse,motivation) VALUES(%s,%s,%s,%s,%s,%s,%s)"
            val = (nom,sexe,email,tel,note_academique,bourse,motivation)
            cursor.execute(sql, val)
            messagebox.showinfo("Enregistrer","Votre reque a été soumise, nous allons vous evaluer\nNous vous repondrons plus tard")
            conn.commit()
            self.destroy()
        except mysql.connector.Error as err:
            print(f'Erreur : {err}')


if __name__ == '__main__':
    app = Fen()
    app.mainloop()