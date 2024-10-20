from pymongo import MongoClient

# Cadena de conexión proporcionada por MongoDB Atlas
client = MongoClient('mongodb+srv://arlettearenass:NHCOu2o0fQ7GOxlK@watchwiz.fx9dj.mongodb.net/')

db = client['Watchwiz']  # Nombre de la base de datos
coleccion = db['registro_empres']  # Nombre de la colección

def get_collection(registro_empres):
    return db[registro_empres]
