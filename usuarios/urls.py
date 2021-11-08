from django.urls import path
from usuarios.views import * 
from usuarios import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.index, name="home"),
    path('listarUsuarios/', UsuariosListar.as_view(), name= 'listar_usuarios'),
    path('listarVehiculos/', VehiculosListar.as_view(), name= 'listar_vehiculos'),
    path('usuario/crear', UsuariosCrear.as_view(), name= 'usuario_crear'),
    path('vehiculo/crear', VehiculosCrear.as_view(), name= 'vehiculo_crear'),
    path('usuario/modificar/<int:pk>', UsuariosModificar.as_view(), name = 'usuario_modificar'),
    path('vehiculo/modificar/<int:pk>', VehiculosModificar.as_view(), name = 'vehiculo_modificar'),
    path('usuario/eliminar/<int:pk>', UsuariosEliminar.as_view(), name='usuario_eliminar'),
    path('vehiculo/eliminar/<int:pk>', VehiculosEliminar.as_view(), name='vehiculo_eliminar'),


]
