from firebase_admin import firestore
import firebase_admin
from django.http import JsonResponse
from watchwiz.services.firebase_service import get_firestore_client


if not firebase_admin._apps:
    firebase_admin.initialize_app()

db = firestore.client()

def eliminar_refaccion(refaccion_id):
    try:
        db.collection('refacciones').document(refaccion_id).delete()
    except Exception as e:
        print(f"Error al eliminar la refacción: {e}")
        raise


def busqueda_global(request):
    #Busqueda en toda la base de datos
    if request.method == "GET" and 'q' in request.GET:
        query = request.GET.get('q', '').lower()
        firestore_client = get_firestore_client()
        resultados = []

        try:
            # Obtener todos los documentos de las colecciones 
            collections = firestore_client.collections()

            for collection in collections:
                documentos = collections.stream()
                for documento in documentos:
                    data = documento.to_dict()

                    # Busqueda en las colecciones los valores
                    if any(query in str(value).lower() for value in data.values()):
                        resultados.append({
                            'id_document': documento.id,
                            'collection': collection.id,
                            'data': data
                        })
            return JsonResponse({'resultados': resultados}, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
    return JsonResponse({'error': 'Consulta no permitida'}, status=405)
