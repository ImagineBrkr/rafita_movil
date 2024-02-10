from .models import *
from rest_framework import permissions, viewsets, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import *


class ProveedorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows proveedores to be viewed or edited.
    """
    queryset = Proveedor.objects.filter(estado=True).order_by('razon_social')
    serializer_class = ProveedorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['razon_social']

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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['descripcion']

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
    http_method_names = ['get', 'post', 'options', 'delete']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['fecha']

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
    http_method_names = ['get', 'options']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['compra']