from .models import Proveedor
from rest_framework import permissions, viewsets
from rest_framework.response import Response

from .serializers import ProveedorSerializer


class ProveedorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows proveedores to be viewed or edited.
    """
    queryset = Proveedor.objects.filter(estado=True)
    serializer_class = ProveedorSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, pk=None):
        proveedor=Proveedor.objects.get(id=pk)
        proveedor.estado=False
        proveedor.save()
        return Response(data = {
            "id": pk,
            "deleted": True
        })


