from django.db import models

class TipoBuque(models.Model):
    id_tipo = models.AutoField(db_column='id_tipo', primary_key=True)
    tipo_buque = models.CharField(db_column='tipo_buque', max_length=20)

    class Meta:
        managed = False
        db_table = 'tipo_buque'
        verbose_name = "Tipo de Buque"
        verbose_name_plural = "Tipos de Buque"
        ordering = ['tipo_buque']

    def __str__(self):
        return self.tipo_buque


class Buque(models.Model):
    id_buque = models.AutoField(db_column='id_buque', primary_key=True)
    id_tipo = models.ForeignKey('TipoBuque', models.PROTECT, db_column='id_tipo')
    nombre_buque = models.CharField(db_column='nombre_buque', max_length=50)
    matricula = models.CharField(db_column='matricula', max_length=10)
    capacidad = models.FloatField(db_column='capacidad')

    class Meta:
        managed = False
        db_table = 'buque'
        verbose_name = "Buque"
        verbose_name_plural = "Buques"
        ordering = ['nombre_buque']

    def __str__(self):
        return f"{self.nombre_buque} ({self.matricula})"


class CategoriaProducto(models.Model):
    id_categoria = models.AutoField(db_column='id_categoria', primary_key=True)
    nombre_categoria = models.CharField(db_column='nombre_categoria', max_length=20)

    class Meta:
        managed = False
        db_table = 'categoria_producto'
        verbose_name = "Categoría de Producto"
        verbose_name_plural = "Categorías de Producto"
        ordering = ['nombre_categoria']

    def __str__(self):
        return self.nombre_categoria


class EstadoViaje(models.Model):
    id_estado = models.AutoField(db_column='id_estado', primary_key=True)
    estado_viaje = models.CharField(db_column='estado_viaje', max_length=20)

    class Meta:
        managed = False
        db_table = 'estado_viaje'
        verbose_name = "Estado del Viaje"
        verbose_name_plural = "Estados del Viaje"
        ordering = ['id_estado']

    def __str__(self):
        return self.estado_viaje


class UnidadMedida(models.Model):
    id_unidad_medida = models.AutoField(db_column='id_unidad_medida', primary_key=True)
    nombre_unidad_medida = models.CharField(db_column='nombre_unidad_medida', max_length=20)

    class Meta:
        managed = False
        db_table = 'unidad_medida'
        verbose_name = "Unidad de Medida"
        verbose_name_plural = "Unidades de Medida"
        ordering = ['nombre_unidad_medida']

    def __str__(self):
        return self.nombre_unidad_medida


class Producto(models.Model):
    id_producto = models.AutoField(db_column='id_producto', primary_key=True)
    id_unidad_medida = models.ForeignKey('UnidadMedida', models.PROTECT, db_column='id_unidad_medida')
    id_categoria = models.ForeignKey('CategoriaProducto', models.PROTECT, db_column='id_categoria')
    nombre_producto = models.CharField(db_column='nombre_producto', max_length=20)
    url_foto = models.CharField(db_column='url_foto', max_length=500)

    class Meta:
        managed = False
        db_table = 'producto'
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre_producto']

    def __str__(self):
        return self.nombre_producto


class Viaje(models.Model):
    id_viaje = models.AutoField(db_column='id_viaje', primary_key=True)
    id_estado = models.ForeignKey('EstadoViaje', models.PROTECT, db_column='id_estado')
    id_buque = models.ForeignKey('Buque', models.PROTECT, db_column='id_buque')
    codigo_viaje = models.IntegerField(db_column='codigo_viaje')
    fecha_inicio = models.DateField(db_column='fecha_inicio')
    fecha_fin = models.DateField(db_column='fecha_fin')
    destino = models.CharField(db_column='destino', max_length=50)

    class Meta:
        managed = False
        db_table = 'viaje'
        verbose_name = "Viaje"
        verbose_name_plural = "Viajes"
        ordering = ['fecha_inicio']

    def __str__(self):
        return f"Viaje {self.codigo_viaje} - {self.destino}"


class Inventario(models.Model):
    id_inventario = models.AutoField(db_column='id_inventario', primary_key=True)
    id_viaje = models.ForeignKey('Viaje', models.PROTECT, db_column='id_viaje')
    id_producto = models.ForeignKey('Producto', models.PROTECT, db_column='id_producto')
    nivel_minimo = models.IntegerField(db_column='nivel_minimo')
    cantidad_disponible = models.IntegerField(db_column='cantidad_disponible')

    class Meta:
        managed = False
        db_table = 'inventario'
        verbose_name = "Inventario"
        verbose_name_plural = "Inventarios"
        ordering = ['id_viaje', 'id_producto']

    def __str__(self):
        return f"{self.id_producto} en viaje {self.id_viaje}"