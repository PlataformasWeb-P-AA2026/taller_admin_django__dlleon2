from django.contrib import admin
from .models import Museo, GuiaDeMuseo, Exhibicion

@admin.register(Museo)
class MuseoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'ciudad', 'año_fundacion', 'costo_total_produccion', 'guia_mas_experimentado')
    search_fields = ('nombre', 'ciudad')
    list_filter = ('ciudad', 'año_fundacion')
    ordering = ('nombre',)

    def costo_total_produccion(self, obj):
        return f"${obj.obtener_costo_total_produccion():,.2f}"
    costo_total_produccion.short_description = "Costo Total Producción"

    def guia_mas_experimentado(self, obj):
        return obj.obtener_guia_mas_experimentado()
    guia_mas_experimentado.short_description = "Guía(s) con más experiencia"


@admin.register(GuiaDeMuseo)
class GuiaDeMuseoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_completo', 'años_experiencia_guia', 'idiomas_hablados', 'museo')
    search_fields = ('nombre_completo', 'idiomas_hablados', 'museo__nombre')
    list_filter = ('museo', 'años_experiencia_guia')
    ordering = ('nombre_completo',)


@admin.register(Exhibicion)
class ExhibicionAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo_exhibicion', 'duracion_meses', 'costo_produccion', 'tematica', 'guia')
    search_fields = ('titulo_exhibicion', 'tematica', 'guia__nombre_completo')
    list_filter = ('tematica', 'duracion_meses', 'guia')
    ordering = ('titulo_exhibicion',)
