import os
from firebase_admin import firestore, storage, auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import firebase_admin
from datetime import datetime


# Inicializar Firebase
if not firebase_admin._apps:
    firebase_admin.initialize_app()

db = firestore.client()

def registrar_empresa(name, email, password, imagen_path, keyword, days_of_week):
    try:
        # Crear el usuario en Firebase Authentication
        user = auth.create_user(
            email=email, 
            password=password
        )

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
    except Exception as e:
     print(f"Error al registrar el usuario en Firebase Authentication y Firestore: {e}")


# Función de autenticación con Firebase Authentication
def autenticar_usuario(email, password):
    try:
        # Autenticar con Firebase Authentication 
        user = auth.get_user_by_email(email)  
        return True  # Autenticación exitosa
    except Exception as e:
        
        return False


 # Validar usuario en Firestore después de autenticar
def validar_usuario(email, password):
    # Autenticar con Firebase Authentication
    if not autenticar_usuario(email, password):
        return False  

    # Proceder con la verificación en Firestore
    user_ref = db.collection('empresa')
    query = user_ref.where('email', '==', email).get()
    
    if query:
        for user in query:
            user_data = user.to_dict()
            stored_password_hash = user_data['password']
            # Verificar contraseña hasheada en Firestore
            if check_password(password, stored_password_hash):
                return True
    return False


# Nueva función para registrar trabajos
def registrar_trabajo(client_name, phone_number, description,
                      photo_url, service_cost, advance, received_date, review_date):

# Funcion para cular el restante
    service_cost = float(service_cost)
    advance = float(advance) if advance is not None else 0
    remaining = service_cost - advance

    received_date = received_date.strftime('%Y-%m-%d')
    review_date = review_date.strftime('%Y-%m-%d')


    trabajo_data = {
        'client_name': client_name,
        'phone_number': phone_number,
        'description': description,
        'photo': photo_url,  
        'service_cost': service_cost,
        'advance': advance,
        'remaining': remaining,
        'received_date': received_date,
        'review_date': review_date
    }

    db.collection('trabajos').add(trabajo_data)

def subir_foto(foto):
    if not foto:
        print("No se recibió ninguna foto para subir")
        return ""
    bucket = storage.bucket('watchwiz-721eb.appspot.com')
    blob = bucket.blob(f'images/{foto.name}')
    blob.upload_from_file(foto)
    foto_url = blob.public_url
    print(f"Foto URL generada: {foto_url}")
    return foto_url

# Obteniendo los datos de los trabajos
def obtener_trabajos():
    trabajos = db.collection('trabajos').stream()
    lista_trabajos = []
    for trabajo in trabajos:
        data = trabajo.to_dict()
        lista_trabajos.append(data)
    return lista_trabajos


def registrar_refacciones(foto, media, precio, calidad, color, caracteristicas,
                          longitud, can_aceptable, existenes):
    try:
        #Subir foto a firebase
        foto_url = subir_foto(foto)

        # Guardar las refacciones
        refaccion_data = {
            'foto': foto_url,
            'medida': media,
            'precio': float(precio),
            'calidad': calidad,
            'color': color,
            'caracteristicas': caracteristicas,
            'longitud': float(longitud),
            'can_aceptable': can_aceptable,
            'existentes': existenes
        }

        #Añadiendo la coleccion de refacciones
        ref = db.collection('refacciones').add(refaccion_data)
        print(f"Refacciones registradas con éxito")
    except Exception as e:
        print(f"Error al registrar las refacciones: {e}")


        