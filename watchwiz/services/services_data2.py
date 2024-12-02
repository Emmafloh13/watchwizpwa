from datetime import date, datetime
from firebase_admin import firestore
from watchwiz.services.firebase_service import subir_imagen

db = firestore.client()

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
    refacciones = []
    refacciones_docs = db.collection('refacciones').stream()
    for doc in refacciones_docs:
        refaccion = doc.to_dict()
        refacciones.append({
            'id': doc.id,
            'imagen': refaccion.get('imagen', ''),
            'nombre': refaccion.get('nombre', ''),
            'categoria': refaccion.get('categoria', ''),
            'medida': refaccion.get('medida', ''),
            'color': refaccion.get('color', ''),
            'precio': refaccion.get('precio', ''),
            'caracteristicas': refaccion.get('caracteristicas', ''),
            'aceptable': refaccion.get('aceptable', ''),
            'existencia': refaccion.get('existencia', ''),
            })
    return refacciones


def obtener_refaccion_por_id(refaccion_id):
    try:
        refaccion_ref = db.collection('refacciones').document(refaccion_id).get()
        if refaccion_ref.exists:
            return refaccion_ref.to_dict()  
        return None
    except Exception as e:
        print(f"Error al obtener refacción: {e}")
        return None

def actualizar_refaccion(refaccion_id, foto, nombre, categoria, precio, medida, color, caracteristicas, aceptable, existencia):
    try:
        # Actualiza los datos de la refacción en Firebase
        data = {
            'imagen': foto,
            'nombre': nombre,
            'categoria': categoria,
            'precio': float(precio),
            'medida': medida,
            'color': color,
            'caracteristicas': caracteristicas,
            'aceptable': aceptable,
            'existencia': float(existencia)
        }

        # Verificar si hay una nueva imagen para actualizar
        if foto:
            # Subir la nueva imagen a Firebase Storage y obtener la URL
            url_imagen = subir_imagen(foto)  
            data["imagen"] = url_imagen

        db.collection('refacciones').document(refaccion_id).update(data)
        print(f"Refacción {refaccion_id} actualizada correctamente.")
    except Exception as e:
        print(f"Error al actualizar refacción: {e}")


def filtrar_refacciones(cantidad):
    # filtrar las refacciones por cantidad
    refacciones = []
    try:
        docs = db.collection('refacciones').where('existencia', '==', cantidad).stream()
        for doc in docs:
            refaccion = doc.to_dict()

            # Calcular las piezas faltantes
            aceptable = refaccion.get('aceptable', 0)
            existencia = refaccion.get('existencia', 0)
            piezas_faltantes = max(0, aceptable - existencia) # hacer que no tengan numeros negativos


            refacciones.append({
                'id': doc.id,
                'imagen': refaccion.get('imagen', ''),
                'nombre': refaccion.get('nombre', ''),
                'piezas_faltantes': piezas_faltantes,
                })
    except Exception as e:
        print(f"Error al obtener las refacciones: {e}")
    return refacciones 


def guardar_entrega(trabajo_data):
        try:
             # Guardar la fecha bien en firebase
             for key, value in trabajo_data.items():
                  trabajo_data[key] = convertir_fecha_a_datetime(value)
                       
             # Guardar los datos de trabajos en la nueva colección 
             db.collection('historial').add(trabajo_data)
             print(f"Trabajo entregado correctamente: {trabajo_data['client_name']}")
             
             # Funcion de eliminarla de la coleccion de trabajos
             trabajo_id = trabajo_data.get('trabajo_id')
             
             if trabajo_id:
                 db.collection('trabajos').document(trabajo_id).delete()
                 print(f"Trabajo eliminado correctamente de la coleccion: {trabajo_id}")
             else:
                 print("No se encontró el ID del trabajo para eliminar.")
                
        except Exception as e:
            print(f"Error al guardar la entrega: {e}")


def convertir_fecha_a_datetime(fecha):
    # Si es una instancia de datetime.date, convertimos a datetime con hora mínima (00:00:00)
    if isinstance(fecha, date) and not isinstance(fecha, datetime):
        return datetime.combine(fecha, datetime.min.time())
    elif isinstance(fecha, datetime):  # Si ya es un datetime, lo dejamos tal cual
        return fecha
    return fecha  # Si no es una fecha, devolvemos el valor tal cual



