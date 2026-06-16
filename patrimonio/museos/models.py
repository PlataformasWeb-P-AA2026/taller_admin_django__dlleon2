from django.db import models

class Museo(models.Model):
    nombre = models.CharField(max_length=150, unique=True, verbose_name="nombre")
    ciudad = models.CharField(max_length=150, verbose_name="ciudad")
    año_fundacion = models.IntegerField(verbose_name="año_fundacion")

    def __str__(self):
        return self.nombre

    def obtener_costo_total_produccion(self):
        from django.db.models import Sum
        total = Exhibicion.objects.filter(guia__museo=self).aggregate(Sum('costo_produccion'))['costo_produccion__sum']
        return total or 0

    def obtener_guia_mas_experimentado(self):
        from django.db.models import Max
        guias = self.guias.all()
        if not guias.exists():
            return "Sin guías"
        max_exp = guias.aggregate(Max('años_experiencia_guia'))['años_experiencia_guia__max']
        if max_exp is None:
            return "Sin guías"
        guias_max = guias.filter(años_experiencia_guia=max_exp)
        return ", ".join([g.nombre_completo for g in guias_max])

    class Meta:
        verbose_name = "Museo"
        verbose_name_plural = "Museos"


class GuiaDeMuseo(models.Model):
    nombre_completo = models.CharField(max_length=200, verbose_name="nombre_completo")
    años_experiencia_guia = models.IntegerField(verbose_name="años_experiencia_guia")
    idiomas_hablados = models.CharField(max_length=300, verbose_name="idiomas_hablados")
    museo = models.ForeignKey(
        Museo, 
        on_delete=models.CASCADE, 
        related_name="guias", 
        verbose_name="museo"
    )

    def __str__(self):
        return self.nombre_completo

    class Meta:
        verbose_name = "Guía de Museo"
        verbose_name_plural = "Guías de Museo"


class Exhibicion(models.Model):
    titulo_exhibicion = models.CharField(max_length=250, verbose_name="titulo_exhibicion")
    duracion_meses = models.IntegerField(verbose_name="duracion_meses")
    costo_produccion = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="costo_produccion"
    )
    tematica = models.CharField(max_length=200, verbose_name="tematica")
    guia = models.ForeignKey(
        GuiaDeMuseo, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="exhibiciones", 
        verbose_name="guia"
    )

    def __str__(self):
        return self.titulo_exhibicion

    class Meta:
        verbose_name = "Exhibición"
        verbose_name_plural = "Exhibiciones"
