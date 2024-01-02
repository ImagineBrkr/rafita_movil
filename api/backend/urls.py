"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from rest_framework import routers

from backend.SeguridadApp import views as seguridadViews
from backend.ComprasApp import views as comprasViews
from backend.PedidosApp import views as pedidosViews
from rest_framework.authtoken.views import obtain_auth_token
from backend.rafita import views as rafitaViews

router = routers.DefaultRouter()
router.register(r'users', seguridadViews.UserViewSet)
router.register(r'groups', seguridadViews.GroupViewSet)
router.register(r'compras/proveedor', comprasViews.ProveedorViewSet)
router.register(r'pedidos/platos', pedidosViews.PlatoViewSet)
router.register(r'pedidos/clientes', pedidosViews.ClienteViewSet)
router.register(r'pedidos/mesas', pedidosViews.MesaViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth', obtain_auth_token, name='api_token_auth'),
    path('hello/', rafitaViews.HelloView.as_view(), name='hello'),
]

urlpatterns += router.urls