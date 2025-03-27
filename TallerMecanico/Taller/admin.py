from django.contrib import admin
from .models import Usuario, Cliente, Vehiculo, Cita, Pieza, Reparacion

# Configuración del administrador para el modelo Usuario
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("username", "rol", "correo_electronico")
    search_fields = ("username", "rol", "correo_electronico")
    list_filter = ("rol",)

# Configuración del administrador para el modelo Cliente
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre_cliente", "telefono", "registrado_por")
    search_fields = ("nombre_cliente", "telefono")
    list_filter = ("registrado_por",)

# Configuración del administrador para el modelo Vehiculo
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ("matricula", "cliente", "marca", "modelo")
    search_fields = ("matricula", "marca", "modelo")
    list_filter = ("marca", "modelo")

# Configuración del administrador para el modelo Cita
class CitaAdmin(admin.ModelAdmin):
    list_display = ("usuario", "cliente", "fecha_cita", "descripcion")
    search_fields = ("usuario__username", "cliente__nombre_cliente", "descripcion")
    list_filter = ("fecha_cita",)

# Configuración del administrador para el modelo Pieza
class PiezaAdmin(admin.ModelAdmin):
    list_display = ("descripcion", "cantidad", "categoria", "stock_actual")
    search_fields = ("descripcion", "categoria")
    list_filter = ("categoria",)

# Configuración del administrador para el modelo Reparacion
class ReparacionAdmin(admin.ModelAdmin):
    list_display = ("vehiculo", "pieza", "fecha_entrada", "fecha_salida", "falla", "precio")
    search_fields = ("vehiculo__matricula", "pieza__descripcion", "falla")
    list_filter = ("fecha_entrada", "fecha_salida")

# Registrar los modelos en el panel de administración
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Vehiculo, VehiculoAdmin)
admin.site.register(Cita, CitaAdmin)
admin.site.register(Pieza, PiezaAdmin)
admin.site.register(Reparacion, ReparacionAdmin)
