# viajes_app/models.py (Este es tu archivo definitivo para la aplicación viajes_app)
from django.db import models

# Importar Buque y TipoBuque si ya los tienes definidos en buque_app/models.py y managed=False
# from buque_app.models import Buque, TipoBuque
# O, si quieres que viajes_app sea más independiente o si tus modelos principales no están en buque_app,
# puedes mantener las definiciones aquí, asegurándote que sean consistentes con tu DB.

# Modelo TipoBuque (se mantiene la definición si no se importa)
class TipoBuque(models.Model):
    id_tipo = models.AutoField(db_column='id_tipo', primary_key=True)
    tipo_buque = models.CharField(db_column='tipo_buque', max_length=15, unique=True)
    class Meta:
        managed = False
        db_table = 'tipo_buque'
        verbose_name = "Tipo de Buque"
        verbose_name_plural = "Tipos de Buque"
    def __str__(self): return self.tipo_buque

# Modelo Buque (se mantiene la definición si no se importa)
class Buque(models.Model):
    id_buque = models.AutoField(db_column='id_buque', primary_key=True)
    tipo_buque = models.ForeignKey(TipoBuque, models.PROTECT, db_column='id_tipo', verbose_name="Tipo de Buque", related_name='buques_asociados')
    nombre = models.CharField(db_column='nombre_buque', max_length=100, verbose_name="Nombre del Buque")
    matricula = models.CharField(db_column='matricula', max_length=50, unique=True, verbose_name="Matrícula")
    capacidad_toneladas = models.FloatField(db_column='capacidad', verbose_name="Capacidad (Toneldas)")
    class Meta:
        managed = False
        db_table = 'buque'
        verbose_name = "Buque"
        verbose_name_plural = "Buques"
        ordering = ['nombre']
    def __str__(self): return f"{self.nombre} ({self.matricula})"

# Modelo EstadoViaje
class EstadoViaje(models.Model):
    id_estado = models.AutoField(db_column='id_estado', primary_key=True)
    estado_viaje = models.CharField(db_column='estado_viaje', max_length=20)
    class Meta:
        managed = False
        db_table = 'estado_viaje'
        verbose_name = "Estado de Viaje"
        verbose_name_plural = "Estados de Viaje"
    def __str__(self): return self.estado_viaje

# Modelo Viaje (el principal para esta aplicación)
class Viaje(models.Model):
    id_viaje = models.AutoField(db_column='id_viaje', primary_key=True)
    id_estado = models.ForeignKey(EstadoViaje, models.PROTECT, db_column='id_estado', verbose_name="Estado del Viaje")
    id_buque = models.ForeignKey(Buque, models.PROTECT, db_column='id_buque', verbose_name="Buque Asignado")
    codigo_viaje = models.IntegerField(db_column='codigo_viaje', unique=True, verbose_name="Código de Viaje")
    fecha_inicio = models.DateField(db_column='fecha_inicio', verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(db_column='fecha_fin', verbose_name="Fecha de Fin")
    destino = models.CharField(db_column='destino', max_length=50, verbose_name="Destino")

    class Meta:
        managed = False
        db_table = 'viaje'
        verbose_name = "Viaje"
        verbose_name_plural = "Viajes"
        ordering = ['fecha_inicio']

    def __str__(self):
        return f"Viaje {self.codigo_viaje} - {self.destino}"
