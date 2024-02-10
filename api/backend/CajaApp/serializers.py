from .models import *
from rest_framework import serializers

class AperturaCajaSerializer(serializers.ModelSerializer):
    cajero = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = AperturaCaja
        fields = ['id', 'cajero', 'estadoApertura', 'importeInicial', 'importe', 'importeFinal', 'fechaInicio', 'fechaCierre']
        read_only_fields = ['cajero', 'estadoApertura', 'importe', 'importeFinal', 'fechaInicio', 'fechaCierre']

    def create(self, validated_data):
        validated_data['cajero'] = self.context['request'].user
        return super().create(validated_data)
    
class ComprobantePagoSerializer(serializers.ModelSerializer):

    def validate_apertura(self, value):
        if not value.estadoApertura:
            raise serializers.ValidationError("La caja está cerrada.")
        return value

    class Meta:
        model = ComprobantePago
        fields = ['pedido', 'apertura', 'tipoPago', 'tipoComprobante', 'fecha', 'importeTotal', 'cliente']
        read_only_fields = ['fecha']