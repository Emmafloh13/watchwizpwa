from datetime import date, datetime
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
                      imagen, service_cost, advance, received_date, review_date, status="En espera"):


# Funcion para cular el restante
    service_cost = float(service_cost)
    advance = float(advance) if advance is not None else 0
    remaining = service_cost - advance

    # Verificar si received_date y review_date son cadenas y convertirlas a objetos date
    if isinstance(received_date, str):
        received_date = datetime.strptime(received_date, '%Y-%m-%d').date()

    if isinstance(review_date, str):
        review_date = datetime.strptime(review_date, '%Y-%m-%d').date()
        
    received_date = received_date.strftime('%Y-%m-%d') if isinstance(received_date, date) else received_date
    review_date = review_date.strftime('%Y-%m-%d') if isinstance(review_date, date) else review_date

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
        'review_date': review_date,
        'status': status or "En espera"
    }

    db.collection('trabajos').add(trabajo_data)



def registrar_refacciones(foto, nombre, categoria, precio, medida, color, caracteristicas,
                          aceptable, existencia, tipo=None, longitud=None, diametro=None, 
                          tamano=None, espesor=None, numero=None, origen=None):
    try:
        # Subir foto a Firebase
        imagen_url = subir_imagen(foto) if foto else None

        # Datos de la refacción
        refaccion_data = {
            'imagen': imagen_url,
            'nombre': nombre,
            'categoria': categoria,
            'precio': float(precio),
            'medida': medida,
            'color': color,
            'caracteristicas': caracteristicas,
            'aceptable': aceptable,
            'existencia': existencia,
            'tipo': tipo,
            'longitud': float(longitud) if longitud else None,
            'diametro': float(diametro) if diametro else None,
            'tamano': tamano,
            'espesor': float(espesor) if espesor else None,
            'numero': numero,
            'origen': origen
        }

        # Remover claves con valores None antes de guardar
        refaccion_data = {k: v for k, v in refaccion_data.items() if v is not None}


        #Añadiendo la coleccion de refacciones
        refaccion_data = db.collection('refacciones').add(refaccion_data)

        print(f"Refacciones registradas con éxito")
    except Exception as e:
        print(f"Error al registrar las refacciones: {e}")



def registrar_categoria(nombre):
    try:
        refaccion_data = {
            'nombre': nombre
        }
        # Guardar la categoria en Firestore
        db.collection('categorias').add(refaccion_data)
        print(f"Categoría '{nombre}' registrada con éxito")
    except Exception as e:
        print(f"Error al registrar la categoría: {e}")

def get_firestore_client():
    if not firebase_admin._apps:
        firebase_admin.initialize_app()
    return firestore.client()
