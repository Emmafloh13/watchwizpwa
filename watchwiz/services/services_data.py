import decimal
from firebase_admin import firestore
from datetime import datetime, timedelta, date


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
            trabajo_data['id'] = trabajo.id  # ID para cada trabajo
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
                    trabajo_data['id'] = trabajo.id  # ID para poder identificar cada trabajo
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

def obtener_trabajo(trabajo_id):
    try:
        trabajo_ref = db.collection('trabajos').document(trabajo_id).get()
        if trabajo_ref.exists:
            trabajo = trabajo_ref.to_dict()
            trabajo['id'] = trabajo_id  # Agrega el ID
        return trabajo
    except Exception as e:
        print(f"Error al obtener trabajo: {e}")
        return None


def actualizar_trabajo(trabajo_id, data):
    try:
        for key, value in data.items():
            if isinstance(value, decimal.Decimal):
                data[key] = float(value)
            elif isinstance(value, (date, datetime)):
                data[key] = value.strftime('%Y-%m-%d')  # Asegúrate de que las fechas estén en formato ISO
            
        db.collection('trabajos').document(trabajo_id).update(data)
        print(f"Trabajo {trabajo_id} actualizado correctamente.")
    except Exception as e:
        print(f"Error al actualizar trabajo: {e}")

def obtener_trabajos_filtrados(status):
    try:
        trabajos_ref = db.collection('trabajos')
        
        # Filtrar por estado si se proporciona
        if status: 
            trabajos = trabajos = trabajos_ref.where('status', '==', status).stream()

        else: 
            trabajos = trabajos_ref.stream()
            
        trabajos_list = []

        for trabajo in trabajos:
            trabajo_data = trabajo.to_dict()
            trabajo_data['id'] = trabajo.id
            trabajos_list.append(trabajo_data)

        return trabajos_list
    except Exception as e:
        print(f"Error al obtener trabajos filtrados por estado: {e}")
        return []
