from .models import *
from rest_framework import permissions, viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import *

class AperturaCajaViewSet(viewsets.ModelViewSet):
    queryset = AperturaCaja.objects.filter().order_by('-fechaInicio')
    serializer_class = AperturaCajaSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['cajero']
    search_fields = ['fechaInicio']
    
    @action(detail=True, methods=['post'], url_path='cerrar_caja')
    def cerrar_caja(self, request, pk=None):
        importeFinal = request.data.get('importeFinal')
        if importeFinal is None:
            return Response({"error": "El campo 'importeFinal' es requerido."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            aperturaCaja = AperturaCaja.objects.get(id=pk)
            if aperturaCaja.estadoApertura == False:
                return Response({"error": "Caja cerrada"}, status=status.HTTP_400_BAD_REQUEST)
            aperturaCaja.importeFinal = importeFinal
            aperturaCaja.importe = ComprobantePago.objects.filter(apertura=aperturaCaja).aggregate(total=Sum('importeTotal'))['total'] or 0
            aperturaCaja.estadoApertura = False
            aperturaCaja.fechaCierre = timezone.now()
            aperturaCaja.save()

            return Response(data=AperturaCajaSerializer(aperturaCaja).data, status=status.HTTP_200_OK)
        except AperturaCaja.DoesNotExist:
            return Response({"error": "Apertura de caja no encontrada."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class ComprobantePagoViewSet(viewsets.ModelViewSet):
    queryset = ComprobantePago.objects.filter().order_by('-fecha')
    serializer_class = ComprobantePagoSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'options', 'post']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['tipoPago', 'tipoComprobante']
    search_fields = ['pedido', 'fecha', 'pedido__cliente__nombre']