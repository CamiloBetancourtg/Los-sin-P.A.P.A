import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from datetime import datetime

from core.Persistencia.DB_manager import DB_Manager

# core/Negocio/actividad_service.py
import datetime
from core.models import Actividad, Usuario

class ActividadService:
    """
    Capa de negocio para manejar la lógica de actividades.
    """

    def crear_actividad(self, datos, usuario, foto=None):
        """
        Crea una nueva actividad validando los datos antes de guardarla.
        """
        # Buscar el usuario (creador)
        try:
            creador = Usuario.objects.get(id=usuario.id)
        except Usuario.DoesNotExist:
            raise ValueError("Usuario no encontrado en la base de datos.")

        # Validaciones
        if not datos.get('nombre_actividad'):
            raise ValueError("El nombre de la actividad es obligatorio.")
        if not datos.get('fecha_hora_inicio'):
            raise ValueError("La fecha de inicio es obligatoria.")

        # Guardar actividad
        actividad = Actividad.objects.create(
            id_creador=creador,
            nombre_actividad=datos['nombre_actividad'],
            descripcion=datos.get('descripcion', ''),
            categoria=datos.get('categoria', ''),
            ubicacion=datos.get('ubicacion', ''),
            fecha_hora_inicio=datos['fecha_hora_inicio'],
            fecha_hora_fin=datos.get('fecha_hora_fin'),
            cupos=datos.get('cupos') or 0,
            foto_actividad=foto.name if foto else '',
            estado='Activa',
            fecha_hora_creacion=datetime.datetime.now(),
            fecha_hora_actualizacion=datetime.datetime.now(),
        )

        return actividad
