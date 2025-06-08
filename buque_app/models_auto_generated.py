# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Buque(models.Model):
    id_buque = models.AutoField(primary_key=True)
    id_tipo = models.ForeignKey('TipoBuque', models.DO_NOTHING, db_column='id_tipo')
    nombre_buque = models.CharField(max_length=50)
    matricula = models.CharField(max_length=10)
    capacidad = models.FloatField()

    class Meta:
        managed = False
        db_table = 'buque'


class CategoriaProducto(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'categoria_producto'


class EstadoViaje(models.Model):
    id_estado = models.AutoField(primary_key=True)
    estado_viaje = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'estado_viaje'


class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey('Producto', models.DO_NOTHING, db_column='id_producto')
    nivel_minimo = models.IntegerField()
    cantidad_disponible = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'inventario'


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    id_unidad_medida = models.ForeignKey('UnidadMedida', models.DO_NOTHING, db_column='id_unidad_medida')
    id_categoria = models.ForeignKey(CategoriaProducto, models.DO_NOTHING, db_column='id_categoria')
    nombre_producto = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'producto'


class TipoBuque(models.Model):
    id_tipo = models.AutoField(primary_key=True)
    tipo_buque = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'tipo_buque'


class UnidadMedida(models.Model):
    id_unidad_medida = models.AutoField(primary_key=True)
    nombre_unidad_medida = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'unidad_medida'


class Viaje(models.Model):
    id_viaje = models.AutoField(primary_key=True)
    id_estado = models.ForeignKey(EstadoViaje, models.DO_NOTHING, db_column='id_estado')
    id_inventario = models.ForeignKey(Inventario, models.DO_NOTHING, db_column='id_inventario')
    id_buque = models.ForeignKey(Buque, models.DO_NOTHING, db_column='id_buque')
    codigo_viaje = models.IntegerField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    destino = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'viaje'
