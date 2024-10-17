from django.db import models

# Create your models here.

class RegistroEmpresa(models.Model):
    ID_registro = models.AutoField(primary_key=True)  
    Nombre_empre = models.CharField(max_length=255)
    Correo = models.EmailField()
    Contraseña = models.CharField(max_length=255)
    Imagen = models.ImageField(upload_to='imagenes/')
    Palabra_clave = models.CharField(max_length=255)
    class Meta:
        app_label = 'watchwiz'

    def __str__(self):
        return self.Nombre_empre


