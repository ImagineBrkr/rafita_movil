from .models import Cliente, Plato, Mesa
from rest_framework import permissions, viewsets
from rest_framework.response import Response

from .serializers import ClienteSerializer, PlatoSerializer, MesaSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows proveedores to be viewed or edited.
    """
    queryset = Cliente.objects.filter(estado=True)
    serializer_class = ClienteSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, pk=None):
        proveedor=Cliente.objects.get(id=pk)
        proveedor.estado=False
        proveedor.save()
        return Response(data = {
            "id": pk,
            "deleted": True
        })

class PlatoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows proveedores to be viewed or edited.
    """
    queryset = Plato.objects.filter(estado=True)
    serializer_class = PlatoSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, pk=None):
        proveedor=Plato.objects.get(id=pk)
        proveedor.estado=False
        proveedor.save()
        return Response(data = {
            "id": pk,
            "deleted": True
        })

class MesaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows proveedores to be viewed or edited.
    """
    queryset = Mesa.objects.filter(estado=True)
    serializer_class = MesaSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, pk=None):
        proveedor=Mesa.objects.get(id=pk)
        proveedor.estado=False
        proveedor.save()
        return Response(data = {
            "id": pk,
            "deleted": True
        })

