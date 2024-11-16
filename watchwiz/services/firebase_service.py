from firebase_admin import firestore, storage, auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import firebase_admin


# Inicializar Firebase
if not firebase_admin._apps:
    firebase_admin.initialize_app()

db = firestore.client()


# Cargar la imagen a Firebase storage
def subir_imagen(imagen):
        try:
            bucket = storage.bucket('watchwiz-721eb.appspot.com')
            blob = bucket.blob(f'images/{imagen.name}')
            blob.upload_from_file(imagen, content_type=imagen.content_type)
            return blob.public_url
        except Exception as e:
            print(f"Error al subir la imagen a Firebase Storage: {e}")
            return None


# Registro de empresas
def registrar_empresa(name, email, password, imagen, keyword, days_of_week):
    try:
        # Crear el usuario en Firebase Authentication
        user = auth.create_user(
            email=email, 
            password=password
        )

        # Hashear contraseña
        hashed_password = make_password(password)

        imagen_url = subir_imagen(imagen) if imagen else None

    # creacion de la empresa con los datos
        empresa_data = {
            'name': name,
            'email': email,
            'password': hashed_password,
            'imagen': imagen_url,
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
                      imagen, service_cost, advance, received_date, review_date):


# Funcion para cular el restante
    service_cost = float(service_cost)
    advance = float(advance) if advance is not None else 0
    remaining = service_cost - advance
    received_date = received_date.strftime('%Y-%m-%d')
    review_date = review_date.strftime('%Y-%m-%d')

#Subir foto de trabajos
    imagen_url = subir_imagen(imagen) if imagen else None
    

    trabajo_data = {
        'client_name': client_name,
        'phone_number': phone_number,
        'description': description,
        'photo': imagen_url,  
        'service_cost': service_cost,
        'advance': advance,
        'remaining': remaining,
        'received_date': received_date,
        'review_date': review_date
    }

    db.collection('trabajos').add(trabajo_data)


def registrar_refacciones(foto, media, precio, calidad, color, caracteristicas,
                          longitud, existenes):
    try:
        #Subir foto a firebase
        imagen_url = subir_imagen(foto) if foto else None

        # Guardar las refacciones
        refaccion_data = {
            'imagen': imagen_url,
            'medida': media,
            'precio': float(precio),
            'calidad': calidad,
            'color': color,
            'caracteristicas': caracteristicas,
            'longitud': float(longitud),
            'existentes': existenes
        }

        #Añadiendo la coleccion de refacciones
        db.collection('refacciones').add(refaccion_data)
        print(f"Refacciones registradas con éxito")
    except Exception as e:
        print(f"Error al registrar las refacciones: {e}")

