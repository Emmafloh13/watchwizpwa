from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]

# Acceso a la colección específica
registro_empresa_collection = db[settings.MONGO_COLLECTION_NAME]
