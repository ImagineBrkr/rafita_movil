from .models import *
from rest_framework import serializers

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = ['id', 'RUC', 'razon_social', 'direccion', 'telefono', 'DNI_representante']

class InsumoSerializer(serializers.ModelSerializer):
    def validate_proveedor(self, value):
        if not value.estado:
            raise serializers.ValidationError("El proveedor seleccionado está eliminado.")
        return value

    class Meta:
        model = Insumo
        fields = ['id', 'descripcion', 'proveedor', 'precio', 'unidad_medida', 'stock']

class DetalleCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleCompra
        fields = ['id', 'insumo', 'cantidad', 'precio', 'compra']
        read_only_fields = ['precio', 'compra']

    def get_total(self, obj):
        return obj.total()

class CompraSerializer(serializers.ModelSerializer):
    usuarioCompra = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    detalles = DetalleCompraSerializer(many=True, source='detallecompra_set')
    
    class Meta:
        model = Compra
        fields = ['id', 'usuarioCompra', 'fecha', 'motivo', 'detalles']
        read_only_fields = ['fecha', 'usuarioCompra']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detallecompra_set')
        validated_data['usuarioCompra'] = self.context['request'].user
        compra = Compra.objects.create(**validated_data)
        for detalle_data in detalles_data:
            insumo_id = detalle_data['insumo'].id
            insumo = Insumo.objects.get(id=insumo_id)
            precio = insumo.precio
            DetalleCompra.objects.create(compra=compra,
                                         precio=precio,
                                           **detalle_data)
            print(insumo.stock)
            insumo.stock += detalle_data['cantidad']
            print(detalle_data['cantidad'])
            print(insumo.stock)
            insumo.save()
        return compra
