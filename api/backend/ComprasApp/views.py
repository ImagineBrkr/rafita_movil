from .models import *
from rest_framework import permissions, viewsets
from rest_framework.response import Response

from .serializers import *


class ProveedorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows proveedores to be viewed or edited.
    """
    queryset = Proveedor.objects.filter(estado=True).order_by('razon_social')
    serializer_class = ProveedorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, pk=None):
        proveedor=Proveedor.objects.get(id=pk)
        proveedor.estado=False
        proveedor.save()
        return Response(data = {
            "id": pk,
            "deleted": True
        })


class InsumoViewSet(viewsets.ModelViewSet):
    queryset = Insumo.objects.filter(estado=True).order_by('descripcion')
    serializer_class = InsumoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, pk=None):
        insumo=Insumo.objects.get(id=pk)
        insumo.estado=False
        insumo.save()
        return Response(data = {
            "id": pk,
            "deleted": True
        })
    
class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.filter(estado=True).order_by('-fecha')
    serializer_class = CompraSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, pk=None):
        compra=Compra.objects.get(id=pk)
        compra.estado=False
        compra.save()
        return Response(data = {
            "id": pk,
            "deleted": True
        })
    
class DetalleCompraViewSet(viewsets.ModelViewSet):
    queryset = DetalleCompra.objects.filter(estado=True)
    serializer_class = DetalleCompraSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, pk=None):
        detalleCompra=DetalleCompra.objects.get(id=pk)
        detalleCompra.estado=False
        detalleCompra.save()
        return Response(data = {
            "id": pk,
            "deleted": True
        })