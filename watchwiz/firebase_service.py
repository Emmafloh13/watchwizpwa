import os
from firebase_admin import firestore, storage
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password


db = firestore.client()

def registrar_empresa(name, email, password,
                      imagen_path, keyword, days_of_week):
    # Hashear contraseña
    hashed_password = make_password(password)

    # Cargar la imagen a Firebase storage
    bucket = storage.bucket('watchwiz-721eb.appspot.com')
    blob = bucket.blob(f'images/{os.path.basename(imagen_path)}')
    blob.upload_from_filename(imagen_path)
    imagen_url = blob.public_url

    # creacion de la empresa con los datos
    empresa_data = {
        'name': name,
        'email': email,
        'password': hashed_password,
        'image': imagen_url,
        'keyword': keyword,
        'days_of_week': days_of_week
    }

    # Guardar la empresa en firebase
    db.collection('empresa').add(empresa_data)


    # Validacion de los usuario
def validar_usuario(email, password):
    # Busqueda del usuario
    user_ref = db.collection('empresa')
    query = user_ref.where('email', '==', email).get()
    
    if query:
        for user in query:
            user_data = user.to_dict()
            stored_password_hash = user_data['password']
            # Verificacion de la contraseña que se guarda

            if check_password(password, stored_password_hash):
                return True
    return False

# Nueva función para registrar trabajos
def registrar_trabajo(client_name, phone_number, description,
                      photo_url, service_cost, advance):

# Funcion para cular el restante
    service_cost = float(service_cost)
    advance = float(advance) if advance is not None else 0
    remaining = service_cost - advance


    trabajo_data = {
        'client_name': client_name,
        'phone_number': phone_number,
        'description': description,
        'photo': photo_url,  
        'service_cost': service_cost,
        'advance': advance,
        'remaining': remaining
    }

    db.collection('trabajos').add(trabajo_data)

def subir_foto(foto):
    bucket = storage.bucket('watchwiz-721eb.appspot.com')
    blob = bucket.blob(f'images/{foto.name}')
    blob.upload_from_file(foto)
    return blob.public_url