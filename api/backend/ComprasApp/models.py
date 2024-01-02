from django.db import models

# Create your models here.

class Proveedor(models.Model):
    RUC = models.CharField(max_length=11, unique=True)
    razon_social = models.CharField(max_length=45)
    direccion = models.CharField(max_length=45)
    telefono = models.CharField(max_length =10, blank = True)
    DNI_representante = models.CharField(max_length=8)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.razon_social
    
