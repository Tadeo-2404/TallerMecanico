from django.contrib import admin
from .models import Usuario, Cliente, Vehiculo, Cita, Pieza, Reparacion


# Configuración del administrador para el modelo Cliente
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre_cliente", "telefono", "registrado_por", "correo_electronico")
    search_fields = ("nombre_cliente", "telefono","correo_electronico")
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
    list_display = ("vehiculo", "pieza", "fecha_entrada", "fecha_salida", "falla", "precio","estado")
    search_fields = ("vehiculo__matricula", "pieza__descripcion", "falla","estado")
    list_filter = ("fecha_entrada", "fecha_salida", "estado")
    def get_vehiculo(self, obj):
        return obj.vehiculo.matricula  # Devuelve la matrícula en lugar de "Vehiculo object (1)"
    
    get_vehiculo.short_description = "Vehículo"  # Nombre de la columna en la tabla

# Registrar los modelos en el panel de administración

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Vehiculo, VehiculoAdmin)
admin.site.register(Cita, CitaAdmin)
admin.site.register(Pieza, PiezaAdmin)
admin.site.register(Reparacion, ReparacionAdmin)
