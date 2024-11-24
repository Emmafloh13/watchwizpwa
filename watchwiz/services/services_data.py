from datetime import datetime
from firebase_admin import firestore
from datetime import timedelta

db = firestore.client()

def obtener_datos_empresa(email):
    try:
        empresa_ref = db.collection('empresa').where('email', '==', email).get()
        for empresa in empresa_ref:
            return empresa.to_dict()  # Devolverá un diccionario con los datos de la empresa
    except Exception as e:
        print(f"Error al obtener datos de la empresa: {e}")
        return None
    
# Obteniendo los datos de los trabajos
def obtener_trabajos():
    try:
        trabajos_ref = db.collection('trabajos')
        trabajos = trabajos_ref.stream()
        trabajos_list = []

        # Fecha actual 
        today = datetime.today().date() 
        
        for trabajo in trabajos:
            trabajo_data = trabajo.to_dict()
            review_date = trabajo_data.get('review_date')

            if review_date:
                if isinstance(review_date, str):
                    try:
                        review_date = datetime.fromisoformat(review_date).date()
                    except ValueError:
                        print(f"Error al convertir review_date: {review_date}")
                        continue
                elif isinstance(review_date, firestore.Timestemp):
                    review_date = review_date.to_datetime().date()

                # Si el trabajo es igual a la fecha actual se da la lista
                if review_date == today:
                    trabajo_data['id'] = trabajo.id  # Agrega el ID para poder identificar cada trabajo
                    trabajo_data['status'] = trabajo_data.get('status', 'Sin especificar')
                    trabajos_list.append(trabajo_data)

        return trabajos_list [:4]
    except Exception as e:
        print(f"Error al obtener los trabajos: {e}")
        return []
    
def obtener_trabajos_manana():
    try:
        trabajos_ref = db.collection('trabajos')
        trabajos = trabajos_ref.stream()
        trabajos_list = []

        # Fecha de mañana
        tomorrow = datetime.today().date() + timedelta(days=1)

        for trabajo in trabajos:
            trabajo_data = trabajo.to_dict()
            review_date = trabajo_data.get('review_date')

            if review_date:
                if isinstance(review_date, str):
                    try:
                        review_date = datetime.fromisoformat(review_date).date()
                    except ValueError:
                        print(f"Error al convertir review_date: {review_date}")
                        continue
                elif isinstance(review_date, firestore.Timestamp):
                    review_date = review_date.to_datetime().date()

                # Si el trabajo es para mañana, añadir a la lista
                if review_date == tomorrow:
                    trabajo_data['id'] = trabajo.id  # Agrega el ID
                    trabajo_data['status'] = trabajo_data.get('status', 'Sin especificar')
                    trabajos_list.append(trabajo_data)

        return trabajos_list[:4]
    except Exception as e:
        print(f"Error al obtener los trabajos de mañana: {e}")
        return []


    
def obtener_categorias():
     categorias = []
     try:
        docs = db.collection('categorias').stream()
        for doc in docs:
            categorias.append({'nombre': doc.to_dict().get('nombre', '')})
     except Exception as e:
            print(f"Error al obtener las categorías: {e}")
     return categorias


def obtener_refacciones():
    db = firestore.client()
    refacciones = []
    refacciones_docs = db.collection('refacciones').stream()
    for doc in refacciones_docs:
        refaccion = doc.to_dict()
        refacciones.append({
            'imagen': refaccion.get('imagen', ''),
            'categoria': refaccion.get('categoria', '')
            })
    return refacciones
    
