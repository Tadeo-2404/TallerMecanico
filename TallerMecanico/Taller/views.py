from django.shortcuts import render, redirect,  get_object_or_404
from django.core.mail import EmailMessage
from django.http import HttpResponse
from .models import Reparacion, Vehiculo, Pieza
from datetime import datetime
from weasyprint import HTML
import qrcode
import base64
from io import BytesIO
from django.template.loader import render_to_string
from django.urls import reverse

def ordenes_servicio(request):
    # Obtener los vehículos y piezas para llenar los selects en el template
    vehiculos = Vehiculo.objects.all()
    piezas = Pieza.objects.all()

    vehiculo_encontrado = None  # Variable para almacenar el vehículo encontrado si existe
    qr_code = None  # Variable para el código QR

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
                vehiculo_encontrado = Vehiculo.objects.get(matricula=matricula)
                
                # Generar URL para el reporte PDF (usando el túnel localhost.run o ngrok)
                cita_url = request.build_absolute_uri(reverse('generar_reporte', args=[vehiculo_encontrado.matricula]))
                
                # Generar código QR
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(cita_url)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                
                # Convertir QR a base64 para mostrar en HTML
                buffer = BytesIO()
                img.save(buffer)
                qr_code = base64.b64encode(buffer.getvalue()).decode('utf-8')
                
            except Vehiculo.DoesNotExist:
                vehiculo_encontrado = None

    # Pasar los datos a la plantilla
    return render(
        request, 
        "ordenes_servicio.html", 
        {
            "vehiculos": vehiculos,
            "piezas": piezas,
            "vehiculo": vehiculo_encontrado,  # Vehículo encontrado o None
            "qr_code": qr_code  # Código QR en base64
        }
    )

def enviar_reporte_email(request, matricula):
    # Buscar el vehículo
    vehiculo = get_object_or_404(Vehiculo, matricula=matricula)

    # Obtener el cliente y su correo
    cliente = vehiculo.cliente  
    destinatario = cliente.correo_electronico  

    if not destinatario:
        return HttpResponse("El cliente no tiene un correo registrado.", status=400)

    # Buscar las reparaciones del vehículo
    reparaciones = Reparacion.objects.filter(vehiculo=vehiculo)

    if not reparaciones.exists():
        return HttpResponse("No se encontraron reparaciones para esta matrícula.", status=404)

    # Generar el contenido HTML del PDF
    html_content = render_to_string('reporte_pdf.html', {'reparaciones': reparaciones})

    # Convertir el HTML a PDF
    pdf_file = BytesIO()
    html = HTML(string=html_content)
    html.write_pdf(pdf_file)
    pdf_file.seek(0)

    # Configurar y enviar el correo
    email = EmailMessage(
        subject="Reporte de reparación",
        body=f"Hola {cliente.nombre_cliente},\n\nAdjunto encontrarás el reporte de la reparación de tu vehículo con matrícula {matricula}.",
        from_email="soffycafri04@gmail.com",
        to=[destinatario]
    )

    # Adjuntar el PDF
    email.attach(f"reporte_{matricula}.pdf", pdf_file.read(), "application/pdf")

    # Enviar el correo
    email.send()

    return HttpResponse(f"Correo enviado a {destinatario} con éxito.")

def generar_qr_code(data):
    """
    Función para generar el código QR y devolverlo en base64.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer)
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return qr_code_base64

def generar_reporte(request, matricula):
    # Buscar el vehículo por la matrícula
    vehiculo = get_object_or_404(Vehiculo, matricula=matricula)

    # Buscar la reparación asociada a ese vehículo
    reparaciones = Reparacion.objects.filter(vehiculo=vehiculo)

    if not reparaciones.exists():
        return HttpResponse("No se encontraron reparaciones para esta matrícula", status=404)

    # Generar la URL correcta para el QR
    cita_url = request.build_absolute_uri(reverse('generar_reporte', args=[matricula]))
    print(f"✅ URL generada para QR: {cita_url}")  # Verificar en consola

    # Generar el QR con la nueva función
    qr_code = generar_qr_code(cita_url)

    # Generar el contenido HTML para el PDF
    html_content = render_to_string('reporte_pdf.html', {'reparaciones': reparaciones, 'qr_code': qr_code})

    # Crear el PDF con WeasyPrint
    html = HTML(string=html_content)
    pdf = html.write_pdf()

    # Crear un archivo de respuesta para el PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_{matricula}.pdf"'
    
    return response

def buscar_vehiculo_v0(request):
    vehiculo = None
    if request.method == "GET" and "matricula" in request.GET:
        matricula = request.GET.get("matricula")
        vehiculo = Vehiculo.objects.filter(matricula=matricula).first()
    return render(request, 'version0.html', {'vehiculo': vehiculo})

def buscar_vehiculo_v1(request):
    vehiculo = None
    if request.method == "GET" and "matricula" in request.GET:
        matricula = request.GET.get("matricula")
        vehiculo = Vehiculo.objects.filter(matricula=matricula).first()
    return render(request, 'version1.html', {'vehiculo': vehiculo})

def buscar_vehiculo_v2(request):
    vehiculo = None
    if request.method == "GET" and "matricula" in request.GET:
        matricula = request.GET.get("matricula")
        vehiculo = Vehiculo.objects.filter(matricula=matricula).first()
    return render(request, 'version2.html', {'vehiculo': vehiculo})

def buscar_vehiculo_v3(request):
    vehiculo = None
    if request.method == "GET" and "matricula" in request.GET:
        matricula = request.GET.get("matricula")
        vehiculo = Vehiculo.objects.filter(matricula=matricula).first()
    return render(request, 'version3.html', {'vehiculo': vehiculo})

def index(request):
    return render(request, 'index.html')

