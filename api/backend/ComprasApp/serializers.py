from .models import Proveedor
from rest_framework import serializers

class ProveedorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Proveedor
        fields = ['RUC', 'razon_social', 'direccion', 'telefono', 'DNI_representante']