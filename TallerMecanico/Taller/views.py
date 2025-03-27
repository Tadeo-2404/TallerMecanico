from django.shortcuts import render, redirect
from .models import Reparacion, Vehiculo, Pieza  # Importa los modelos
from datetime import datetime

def ordenes_servicio(request):
    # Obtener los vehículos y piezas para llenar los selects en el template
    vehiculos = Vehiculo.objects.all()
    piezas = Pieza.objects.all()

    if request.method == "POST":
        # Capturar datos del formulario
        vehiculo_id = request.POST.get("vehiculo")
        pieza_id = request.POST.get("pieza")
        fecha_entrada = request.POST.get("fecha_entrada")
        fecha_salida = request.POST.get("fecha_salida") or None
        falla = request.POST.get("falla")
        precio = request.POST.get("precio")

        # Validar que se hayan seleccionado los datos correctos
        if vehiculo_id and pieza_id:
            vehiculo = Vehiculo.objects.get(id=vehiculo_id)
            pieza = Pieza.objects.get(id=pieza_id)

            # Guardar la reparación en la base de datos
            Reparacion.objects.create(
                vehiculo=vehiculo,
                pieza=pieza,
                fecha_entrada=datetime.strptime(fecha_entrada, "%Y-%m-%d"),
                fecha_salida=datetime.strptime(fecha_salida, "%Y-%m-%d") if fecha_salida else None,
                falla=falla,
                precio=precio
            )

            return redirect("ordenes_servicio")  # Redirigir para evitar reenvío del formulario

    # Pasar los datos a la plantilla
    return render(request, "ordenes_servicio.html", {"vehiculos": vehiculos, "piezas": piezas})


def index(request):
    return render(request, 'index.html')

