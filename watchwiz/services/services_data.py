from firebase_admin import firestore

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
        for trabajo in trabajos:
            trabajo_data = trabajo.to_dict()
            trabajo_data['id'] = trabajo.id  # Agrega el ID para poder identificar cada trabajo
            trabajos_list.append(trabajo_data)
        return trabajos_list
    except Exception as e:
        print(f"Error al obtener los trabajos: {e}")
        return []