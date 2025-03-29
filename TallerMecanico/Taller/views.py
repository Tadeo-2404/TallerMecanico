from django.shortcuts import render, redirect,  get_object_or_404
from django.http import HttpResponse
from .models import Reparacion, Vehiculo, Pieza
from datetime import datetime
from weasyprint import HTML
import qrcode
import base64
from io import BytesIO
from django.template.loader import render_to_string

def ordenes_servicio(request):
    # Obtener los vehículos y piezas para llenar los selects en el template
    vehiculos = Vehiculo.objects.all()
    piezas = Pieza.objects.all()

    vehiculo_encontrado = None  # Variable para almacenar el vehículo encontrado si existe

    if request.method == "POST":
        # Capturar datos del formulario de registro de reparación
        vehiculo_id = request.POST.get("vehiculo")
        pieza_id = request.POST.get("pieza")
        fecha_entrada = request.POST.get("fecha_entrada")
        fecha_salida = request.POST.get("fecha_salida") or None
        falla = request.POST.get("falla")
        precio = request.POST.get("precio")
        estado = request.POST.get("estado", "pendiente")

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
                precio=precio,
                estado=estado
            )

            return redirect("ordenes_servicio")  # Redirigir para evitar reenvío del formulario
    
    elif request.method == "GET" and 'matricula' in request.GET:
        # Buscar vehículo por matrícula (matricula en lugar de placa)
        matricula = request.GET.get("matricula").strip()

        if matricula:
            try:
                # Buscar el vehículo en la base de datos por matrícula
                vehiculo_encontrado = Vehiculo.objects.get(matricula=matricula)  # Corregido a 'matricula'
            except Vehiculo.DoesNotExist:
                vehiculo_encontrado = None

    # Pasar los datos a la plantilla
    return render(
        request, 
        "ordenes_servicio.html", 
        {
            "vehiculos": vehiculos,
            "piezas": piezas,
            "vehiculo": vehiculo_encontrado  # Vehículo encontrado o None
        }
    )

def generar_reporte(request, matricula):
    # Buscar el vehículo por la matrícula
    vehiculo = get_object_or_404(Vehiculo, matricula=matricula)

    # Buscar la reparación asociada a ese vehículo
    reparaciones = Reparacion.objects.filter(vehiculo=vehiculo)

    if not reparaciones.exists():
        return HttpResponse("No se encontraron reparaciones para esta matrícula", status=404)

    # Generar el enlace de la cita con la matrícula
    cita_url = request.build_absolute_uri(f"/cita/{matricula}/")

    # Crear el código QR para la cita
    qr = qrcode.make(cita_url)
    buffer = BytesIO()
    qr.save(buffer)
    qr_code = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Generar el contenido HTML para el PDF
    html_content = render_to_string('reporte_pdf.html', {'reparaciones': reparaciones, 'qr_code': qr_code})

    # Crear el PDF con WeasyPrint
    html = HTML(string=html_content)
    pdf = html.write_pdf()

    # Crear un archivo de respuesta para el PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_{matricula}.pdf"'
    
    return response

def index(request):
    return render(request, 'index.html')

