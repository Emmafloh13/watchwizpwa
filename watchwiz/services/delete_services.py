from firebase_admin import firestore
import firebase_admin


if not firebase_admin._apps:
    firebase_admin.initialize_app()

db = firestore.client()

def eliminar_refaccion(refaccion_id):
    try:
        db.collection('refacciones').document(refaccion_id).delete()
    except Exception as e:
        print(f"Error al eliminar la refacción: {e}")
        raise