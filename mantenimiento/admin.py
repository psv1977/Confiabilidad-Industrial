from django.contrib import admin
from .models import Activo

@admin.register(Activo)
class ActivoAdmin(admin.ModelAdmin):
    # Columnas que verás en la tabla
    list_display = ('codigo_interno', 'nombre', 'marca', 'criticidad', 'fecha_instalacion')
    # Buscador por nombre y código
    search_fields = ('nombre','codigo_interno')
    # Filtros laterales
    list_filter = ('criticidad','marca')  


