from .models import *
from rest_framework import permissions, viewsets, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


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

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.filter(estado=True)
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
