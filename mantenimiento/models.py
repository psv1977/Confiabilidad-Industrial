from django.db import models

class Activo(models.Model):
    NIVEL_CRITICIDAD = [
        ('ALTA', 'Alta'),
        ('MEDIA', 'Media'),
        ('BAJA', 'Baja'),
    ]

    nombre = models.CharField(max_length=100, verbose_name="Nombre del Equipo")
    codigo_interno = models.CharField(max_length=50, unique=True, verbose_name="Código (Tag)")
    marca = models.CharField(max_length=50)
    fecha_instalacion = models.DateField(verbose_name="Fecha de Instalación")
    criticidad = models.CharField(max_length=5, choices=NIVEL_CRITICIDAD, default='MEDIA')

    def __str__(self):
        return f"{self.codigo_interno} - {self.nombre}"

    class Meta:
        verbose_name = "Activo"
        verbose_name_plural = "Activos"

        