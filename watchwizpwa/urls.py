from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from watchwizpwa.views.auth_views import home_view, login_view, principal_view, registro_view, logout_view
from watchwizpwa.views.trabajos_views import registro_trabajos, trabajos_views
from watchwizpwa.views.tra_data_views import trabajo_detail_view
from watchwizpwa.views.historiaT_views import detalles_trabajos, historial_trabajos
from watchwizpwa.views.invet_views import categoria_view, detalles_refaccion_view, editar_refaccion_view, eliminar_refaccion_view, inventario_view, refacciones_view

urlpatterns = [
    path('', principal_view, name='principal'),
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('registro/', registro_view, name='registro'),
    path('logout/', logout_view, name='logout'),
    # VISTA DEL FORMULARIO  Y DE REGISTROS 
    path('registro_trabajos/', registro_trabajos, name='registro_trabajos'),
    path('trabajos/', trabajos_views, name='trabajos'),
    # VISTA DE INVENTARIO
    path('refacciones/', refacciones_view, name='refacciones'),
    path('registrar_categoria/', categoria_view, name='registrar_categoria'),
    path('inventario/', inventario_view, name='inventario'),
    # VISTA DE LOS TRABAJOS A DETALLE
    path('detalles_refacciones/<str:refaccion_id>/', detalles_refaccion_view, name='detalles_refacciones'),
    path('trabajo/<str:trabajo_id>/', trabajo_detail_view, name='trabajos_data'),
    path('historial/', historial_trabajos, name='historial_trabajos'),
    path('trabajo/<str:trabajo_id>/', detalles_trabajos, name='detalles_trabajo'),
    # VISTA PARA EDITAR Y ELIMINAR
     path('editar_refaccion/<str:refaccion_id>/', editar_refaccion_view, name='editar_refaccion'),
    path('eliminar_refaccion/<str:refaccion_id>/', eliminar_refaccion_view, name='eliminar_refaccion'),
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
