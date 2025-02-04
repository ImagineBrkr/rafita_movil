from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, F

# Create your models here.

class Cliente(models.Model):
    nombre=models.CharField(max_length=80)
    direccion=models.CharField(max_length=50, blank = True)
    email=models.EmailField(blank = True)
    telefono=models.CharField(max_length=15, blank = True)
    TIPO_CLIENTE_CHOICES = [
        ('Natural', 'Natural'),
        ('Jurídico', 'Jurídico'),
    ]
    TIPO_DOCUMENTO_CHOICES = [
        ('DNI', 'DNI'),
        ('RUC', 'RUC'),
        ('Carné de Extranjería', 'Carné de Extranjería'),
    ]
    tipoCliente = models.CharField(max_length=10, choices = TIPO_CLIENTE_CHOICES)
    tipoDocumento = models.CharField(max_length = 25, choices = TIPO_DOCUMENTO_CHOICES)
    nroDocumento=models.CharField(max_length=11, unique=True)
    estado=models.BooleanField(default=True)
    def __str__(self):
        return self.nroDocumento + " - " + self.nombre
    
class Plato(models.Model):
    TIPO_CHOICES = [
        ('Plato', 'Plato'),
        ('Bebida', 'Bebida'),
        ('Acompañamiento', 'Acompañamiento'),
        ('Otros', 'Otros'),
    ]
    nombre      = models.CharField(max_length=40, unique=True)
    estado      = models.BooleanField(default=True)
    categoria   = models.CharField(max_length=15, choices = TIPO_CHOICES, default = 'Plato')
    precio      = models.DecimalField(max_digits=4, decimal_places=2)
    def __str__(self):
        return self.categoria + " - " + self.nombre
    
class Mesa(models.Model):
    nombre = models.CharField(max_length=10)
    enUso = models.BooleanField(default = False)
    horaUltimoUso = models.DateTimeField(auto_now=True)
    estado = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre
    class Meta:
        permissions = (("liberar_mesa", "Liberar mesa"),)

class Pedido(models.Model):
    usuarioRegistra = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usuarioRegistra")
    Fecha = models.DateTimeField(auto_now_add = True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE, null = True)
    pagado = models.BooleanField(default=False)
    estado = models.BooleanField(default=True)
    def total_pedido(self):
        total = self.detallepedido_set.filter(estado=True).aggregate(
            total=Sum(F('precio') * F('cantidad'), output_field=models.DecimalField())
        )['total']
        return total or 0

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    indicaciones = models.CharField(max_length=50, blank = True)
    precio = models.DecimalField(max_digits=4, decimal_places=2)
    estado = models.BooleanField(default = True)

    def total(self):
        return self.precio * self.cantidad