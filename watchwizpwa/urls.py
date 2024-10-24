from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from watchwizpwa.views import home_view, login_view, principal_view, registro_trabajos, registro_view


urlpatterns = [
    #path('admin/', admin.site.urls),
    
    path('', principal_view, name='principal'),
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('registro/', registro_view, name='registro'),
    path('logout/', login_view, name='login'),
    path('registro_trabajos/', registro_trabajos, name='registro_trabajos')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
