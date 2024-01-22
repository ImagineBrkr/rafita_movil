from .models import Plato, Cliente, Mesa
from rest_framework import serializers

class PlatoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Plato
        fields = ['id', 'nombre', 'categoria', 'precio']

class MesaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mesa
        fields = ['id', 'nombre']

class ClienteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'direccion', 'email', 'telefono', 'tipoCliente', 'tipoDocumento', 'nroDocumento']