from .models import Plato, Cliente, Mesa
from rest_framework import serializers

class PlatoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Plato
        fields = ['nombre', 'categoria', 'precio']

class MesaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mesa
        fields = ['nombre']

class ClienteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cliente
        fields = ['nombre', 'direccion', 'email', 'telefono', 'tipoCliente', 'tipoDocumento', 'nroDocumento']