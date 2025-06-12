from django.db import models

class TipoBuque(models.Model):
    # ID_TIPO en DB, ahora mapeado a 'id_tipo' en minúsculas
    id_tipo = models.AutoField(db_column='id_tipo', primary_key=True)
    # TIPO_BUQUE en DB, ahora mapeado a 'tipo_buque' en minúsculas
    tipo_buque = models.CharField(db_column='tipo_buque', max_length=15, unique=True)

    class Meta:
        managed = False
        db_table = 'tipo_buque' # Ya estaba en minúsculas
        verbose_name = "Tipo de Buque"
        verbose_name_plural = "Tipos de Buque"

    def __str__(self):
        return self.tipo_buque

class Buque(models.Model):
    # ID_BUQUE en DB, ahora mapeado a 'id_buque' en minúsculas
    id_buque = models.AutoField(db_column='id_buque', primary_key=True)
    # ID_TIPO en DB (Foreign Key), ahora mapeado a 'id_tipo' en minúsculas
    tipo_buque = models.ForeignKey(TipoBuque, models.PROTECT, db_column='id_tipo', verbose_name="Tipo de Buque", related_name='buques_asociados')
    # NOMBRE_BUQUE en DB, ahora mapeado a 'nombre_buque' en minúsculas
    nombre = models.CharField(db_column='nombre_buque', max_length=100, verbose_name="Nombre del Buque")
    # MATRICULA en DB, ahora mapeado a 'matricula' en minúsculas
    matricula = models.CharField(db_column='matricula', max_length=50, unique=True, verbose_name="Matrícula")
    # CAPACIDAD en DB, ahora mapeado a 'capacidad' en minúsculas
    capacidad_toneladas = models.FloatField(db_column='capacidad', verbose_name="Capacidad (Toneldas)")

    class Meta:
        managed = False
        db_table = 'buque' # Ya estaba en minúsculas
        verbose_name = "Buque"
        verbose_name_plural = "Buques"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.matricula})"
