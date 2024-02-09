from .models import *
from rest_framework import permissions, viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.CajaApp.models import ComprobantePago
from backend.CajaApp.serializers import ComprobantePagoSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404

from .serializers import *

def ocupar_liberar_mesa(id_mesa, enUso):
    mesa = Mesa.objects.get(id=id_mesa)
    mesa.enUso = enUso
    mesa.save()

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.filter(estado=True).order_by('nombre')
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['nombre']

    def destroy(self, request, pk=None):
        cliente=Cliente.objects.get(id=pk)
        cliente.estado=False
        cliente.save()
        return Response(data = {
            "id": pk,
            "deleted": True
        })

class PlatoViewSet(viewsets.ModelViewSet):
    queryset = Plato.objects.filter(estado=True)
    serializer_class = PlatoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, pk=None):
        plato=Plato.objects.get(id=pk)
        plato.estado=False
        plato.save()
        return Response(data = {
            "id": pk,
            "deleted": True
        })

class MesaViewSet(viewsets.ModelViewSet):
    queryset = Mesa.objects.filter(estado=True)
    serializer_class = MesaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, pk=None):
        mesa=Mesa.objects.get(id=pk)
        mesa.estado=False
        mesa.save()
        return Response(data = {
            "id": pk,
            "deleted": True
        })

    @action(detail=True, methods=['get'], url_path='obtener_pedido')
    def obtener_pedido(self, request, pk=None):
        mesa = self.get_object()
        if mesa.enUso:
            try:
                pedido = Pedido.objects.filter(estado=True, mesa=pk).latest('Fecha')
            except:
                raise Http404
        else:
            raise Http404
        return Response(data = PedidoSerializer(pedido).data)

    @action(detail=True, methods=['get'], url_path='liberar_mesa')
    def liberar_mesa(self, request, pk=None):
        ocupar_liberar_mesa(pk, False)
        return Response(self.get_serializer(self.get_object()).data)

    @action(detail=True, methods=['get'], url_path='ocupar_mesa')
    def ocupar_mesa(self, request, pk=None):
        ocupar_liberar_mesa(pk, True)
        return Response(self.get_serializer(self.get_object()).data)

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.filter(estado=True).order_by('-Fecha')
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['pagado', 'usuarioRegistra']
    search_fields = ['Fecha', 'cliente__nombre']

    def perform_create(self, serializer):
        ocupar_liberar_mesa(serializer.validated_data['mesa'].id, True)
        serializer.save()

    def destroy(self, request, pk=None):
        pedido=Pedido.objects.get(id=pk)
        pedido.estado=False
        pedido.save()
        ocupar_liberar_mesa(pedido.mesa.id, False)
        return Response(data = {
            "id": pk,
            "deleted": True
        })
    
    @action(detail=True, methods=['post'], url_path='pagar_pedido')
    def pagar_pedido(self, request, pk=None):
        pedido = self.get_object()
        importeTotal = pedido.total_pedido()
        data = request.data.copy()
        data['pedido'] = pedido.id
        data['importeTotal'] = importeTotal
        data['cliente'] = pedido.cliente.id
    
        serializer = ComprobantePagoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            pedido.pagado = True
            pedido.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DetallePedidoViewSet(viewsets.ModelViewSet):
    queryset = DetallePedido.objects.filter(estado=True)
    serializer_class = DetallePedidoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, pk=None):
        detallePedido=DetallePedido.objects.get(id=pk)
        detallePedido.estado=False
        detallePedido.save()
        return Response(data = {
            "id": pk,
            "deleted": True
        })
