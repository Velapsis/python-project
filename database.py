import sqlite3

# Connexion à la base de données
db = sqlite3.connect("database.db")

# Création du curseur pour intéragir avec la base de données
cursor = db.cursor()

