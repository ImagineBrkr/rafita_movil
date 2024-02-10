from .models import *
from rest_framework import serializers

class PlatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plato
        fields = ['id', 'nombre', 'categoria', 'precio']

class MesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesa
        fields = ['id', 'nombre', 'enUso', 'horaUltimoUso']
        read_only_fields = ['enUso', 'horaUltimoUso']

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'direccion', 'email', 'telefono', 'tipoCliente', 'tipoDocumento', 'nroDocumento']

class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = ['id', 'plato', 'cantidad', 'indicaciones', 'precio', 'pedido']
        read_only_fields = ['precio', 'pedido']

    def get_total(self, obj):
        return obj.total()

    def create(self, validated_data):
        plato_id = validated_data['plato'].id
        plato = Plato.objects.get(id=plato_id)
        validated_data['precio'] = plato.precio
        return super().create(validated_data)

class PedidoSerializer(serializers.ModelSerializer):
    usuarioRegistra = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    Fecha = serializers.DateTimeField(read_only=True)
    pagado = serializers.BooleanField(read_only=True)
    detalles = DetallePedidoSerializer(many=True, source='detallepedido_set')
    
    class Meta:
        model = Pedido
        fields = ['id', 'usuarioRegistra', 'Fecha', 'cliente', 'mesa', 'pagado', 'detalles']

    def validate_mesa(self, value):
        """
        Comprueba que la mesa seleccionada no esté en uso.
        """
        if value.enUso:
            raise serializers.ValidationError("La mesa seleccionada está actualmente en uso.")
        return value

    def create(self, validated_data):
        detalles_data = validated_data.pop('detallepedido_set')
        validated_data['usuarioRegistra'] = self.context['request'].user
        pedido = Pedido.objects.create(**validated_data)
        for detalle_data in detalles_data:
            plato_id = detalle_data['plato'].id
            plato = Plato.objects.get(id=plato_id)
            precio = plato.precio
            DetallePedido.objects.create(pedido=pedido,
                                         precio=precio,
                                           **detalle_data)
        return pedido
