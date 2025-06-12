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

    def __str__(self): return self.tipo_buque

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

    def __str__(self): return f"{self.nombre} ({self.matricula})"

class EstadoViaje(models.Model):
    # ID_ESTADO en DB, ahora mapeado a 'id_estado' en minúsculas
    id_estado = models.AutoField(db_column='id_estado', primary_key=True)
    # ESTADO_VIAJE en DB, ahora mapeado a 'estado_viaje' en minúsculas
    estado_viaje = models.CharField(db_column='estado_viaje', max_length=20)

    class Meta:
        managed = False
        db_table = 'estado_viaje' # <--- CAMBIADO A MINÚSCULAS
        verbose_name = "Estado de Viaje"
        verbose_name_plural = "Estados de Viaje"

    def __str__(self): return self.estado_viaje

class Viaje(models.Model):
    # ID_VIAJE en DB, ahora mapeado a 'id_viaje' en minúsculas
    id_viaje = models.AutoField(db_column='id_viaje', primary_key=True)
    # ID_ESTADO en DB (Foreign Key), ahora mapeado a 'id_estado' en minúsculas
    id_estado = models.ForeignKey(EstadoViaje, models.PROTECT, db_column='id_estado', verbose_name="Estado del Viaje")
    # ID_BUQUE en DB (Foreign Key), ahora mapeado a 'id_buque' en minúsculas
    id_buque = models.ForeignKey(Buque, models.PROTECT, db_column='id_buque', verbose_name="Buque Asignado")
    
    # CODIGO_VIAJE en DB, ahora mapeado a 'codigo_viaje' en minúsculas
    codigo_viaje = models.IntegerField(db_column='codigo_viaje', unique=True, verbose_name="Código de Viaje")
    # FECHA_INICIO en DB, ahora mapeado a 'fecha_inicio' en minúsculas
    fecha_inicio = models.DateField(db_column='fecha_inicio', verbose_name="Fecha de Inicio")
    # FECHA_FIN en DB, ahora mapeado a 'fecha_fin' en minúsculas
    fecha_fin = models.DateField(db_column='fecha_fin', verbose_name="Fecha de Fin")
    # DESTINO en DB, ahora mapeado a 'destino' en minúsculas
    destino = models.CharField(db_column='destino', max_length=50, verbose_name="Destino")

    class Meta:
        managed = False
        db_table = 'viaje' # <--- CAMBIADO A MINÚSCULAS
        verbose_name = "Viaje"
        verbose_name_plural = "Viajes"
        ordering = ['fecha_inicio']

    def __str__(self):
        return f"Viaje {self.codigo_viaje} - {self.destino}"

