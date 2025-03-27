from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('secretaria', 'Secretaria'),
        ('mecanico', 'Mecánico'),
    ]
    rol = models.CharField(max_length=10, choices=ROL_CHOICES)
    correo_electronico = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)

    # Agregar related_name para evitar conflictos con auth.User
    groups = models.ManyToManyField(Group, related_name="usuario_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="usuario_permissions", blank=True)

# Modelo de clientes
class Cliente(models.Model):
    nombre_cliente = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10)
    registrado_por = models.ForeignKey(Usuario, on_delete=models.CASCADE)

# Modelo de vehículos
class Vehiculo(models.Model):
    matricula = models.CharField(max_length=20, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    marca = models.CharField(max_length=20)
    modelo = models.CharField(max_length=20)

# Modelo de citas
class Cita(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_cita = models.DateTimeField()
    descripcion = models.CharField(max_length=255)

# Modelo de piezas
class Pieza(models.Model):
    descripcion = models.CharField(max_length=255)
    cantidad = models.IntegerField()
    categoria = models.CharField(max_length=50, null=True, blank=True)
    stock_actual = models.IntegerField()

# Modelo de reparaciones
class Reparacion(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    pieza = models.ForeignKey(Pieza, on_delete=models.CASCADE)
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField(null=True, blank=True)
    falla = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
