from django.shortcuts import render
from django.http import HttpResponse
from core.Negocio.auth import *
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.Negocio.actividad_service import ActividadService
from django.utils import timezone
from core.models import Usuario
# Create your views here.

def view_register(request):
    if request.method == 'GET':
        return render(request, 'core/register.html', {
            'form': CustomUserCreationForm
        })
    else:
        return auth.register_user(request=request)
def home(request):
    return render(request, 'core/home.html')



##@login_required


def crear_actividad(request):
    service = ActividadService()

    if request.method == "POST":
        datos = {
            'nombre_actividad': request.POST.get('nombre_actividad'),
            'descripcion': request.POST.get('descripcion'),
            'categoria': request.POST.get('categoria'),
            'ubicacion': request.POST.get('ubicacion'),
            'fecha_hora_inicio': request.POST.get('fecha_hora_inicio'),
            'fecha_hora_fin': request.POST.get('fecha_hora_fin'),
            'cupos': request.POST.get('cupos'),
        }
        foto = request.FILES.get('foto_actividad')

        try:
            # ⚠️ Usa un usuario temporal si no hay sesión iniciada
            usuario = request.user if request.user.is_authenticated else Usuario.objects.first()
            service.crear_actividad(datos=datos, usuario=usuario, foto=foto)
            return redirect('actividad_creada')
        except Exception as e:
            return render(request, 'core/crear_actividad.html', {'error': str(e)})

    return render(request, 'core/crear_actividad.html')



def actividad_creada(request):
    return render(request, 'core/actividad_creada.html')