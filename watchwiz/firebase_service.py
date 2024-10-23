import os
from firebase_admin import firestore, storage
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import check_password


db = firestore.client()

def registrar_empresa(nombre_empresa, email, password, imagen_path, palabra_clave):
    # Hashear contraseña
    hashed_password = make_password(password)

    # Cargar la imagen a Firebase storage
    bucket = storage.bucket('watchwiz-721eb.appspot.com')
    blob = bucket.blob(f'images/{os.path.basename(imagen_path)}')
    blob.upload_from_filename(imagen_path)
    imagen_url = blob.public_url

    # creacion de la empresa con los datos
    empresa_data = {
        'Nombre_empresa': nombre_empresa,
        'Email': email,
        'Password': hashed_password,
        'Imagen': imagen_url,
        'Palabra_clave': palabra_clave,
    }

    # Guardar la empresa en firebase
    db.collection('Empresas').add(empresa_data)


    # Validacion de los usuario
def validar_usuario(email, password):
    # Busqueda del usuario
    user_ref = db.collection('Empresas')
    query = user_ref.where('Email', '==', email).get()
    
    if query:
        for user in query:
            user_data = user.to_dict()
            stored_password_hash = user_data['Password']
            # Verificacion de la contraseña que se guarda

            if check_password(password, stored_password_hash):
                return True
    return False

