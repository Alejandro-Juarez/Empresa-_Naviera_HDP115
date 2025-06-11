from django.db import models

# Importamos el modelo Viaje desde la aplicación viaje_app.
from viaje_app.models import Viaje


# --- Modelos que mapean a tablas de referencia (MAESTRAS) para Inventario ---

class CategoriaProducto(models.Model):
    # ID_CATEGORIA en DB, ahora mapeado a 'id_categoria' en minúsculas
    id_categoria = models.AutoField(db_column='id_categoria', primary_key=True)
    # NOMBRE_CATEGORIA en DB, ahora mapeado a 'nombre_categoria' en minúsculas
    nombre_categoria = models.CharField(db_column='nombre_categoria', max_length=50, unique=True, verbose_name="Nombre de Categoría")

    class Meta:
        managed = False
        db_table = 'categoria_producto' # Cambiado a minúsculas
        verbose_name = "Categoría de Producto"
        verbose_name_plural = "Categorías de Producto"

    def __str__(self):
        return self.nombre_categoria


class UnidadMedida(models.Model):
    # ID_UNIDAD_MEDIDA en DB, ahora mapeado a 'id_unidad_medida' en minúsculas
    id_unidad_medida = models.AutoField(db_column='id_unidad_medida', primary_key=True)
    # NOMBRE_UNIDAD_MEDIDA en DB, ahora mapeado a 'nombre_unidad_medida' en minúsculas
    nombre_unidad_medida = models.CharField(db_column='nombre_unidad_medida', max_length=50, unique=True, verbose_name="Nombre de Unidad de Medida")

    class Meta:
        managed = False
        db_table = 'unidad_medida' # Cambiado a minúsculas
        verbose_name = "Unidad de Medida"
        verbose_name_plural = "Unidades de Medida"

    def __str__(self):
        return self.nombre_unidad_medida


class Producto(models.Model):
    # ID_PRODUCTO en DB, ahora mapeado a 'id_producto' en minúsculas
    id_producto = models.AutoField(db_column='id_producto', primary_key=True)
    
    # ID_UNIDAD_MEDIDA en DB (Foreign Key), ahora mapeado a 'id_unidad_medida' en minúsculas
    id_unidad_medida = models.ForeignKey(
        UnidadMedida,
        models.PROTECT,
        db_column='id_unidad_medida', # Nombre exacto de la columna FK en tu tabla PRODUCTO
        verbose_name="Unidad de Medida"
    )
    
    # ID_CATEGORIA en DB (Foreign Key), ahora mapeado a 'id_categoria' en minúsculas
    id_categoria = models.ForeignKey(
        CategoriaProducto,
        models.PROTECT,
        db_column='id_categoria', # Nombre exacto de la columna FK en tu tabla PRODUCTO
        verbose_name="Categoría"
    )
    
    # NOMBRE_PRODUCTO en DB, ahora mapeado a 'nombre_producto' en minúsculas
    nombre_producto = models.CharField(db_column='nombre_producto', max_length=100, unique=True, verbose_name="Nombre del Producto")
    # URL_FOTO en DB, ahora mapeado a 'url_foto' en minúsculas
    url_foto = models.CharField(db_column='url_foto', max_length=500, blank=True, null=True, verbose_name="URL de Foto")

    class Meta:
        managed = False
        db_table = 'producto' # Cambiado a minúsculas
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre_producto']

    def __str__(self):
        return self.nombre_producto


# --- Modelo Principal: Inventario ---

class Inventario(models.Model):
    # ID_INVENTARIO en DB, ahora mapeado a 'id_inventario' en minúsculas
    id_inventario = models.AutoField(db_column='id_inventario', primary_key=True)
    
    # ID_VIAJE en DB (Foreign Key), ahora mapeado a 'id_viaje' en minúsculas
    id_viaje = models.ForeignKey(
        Viaje,
        models.PROTECT,
        db_column='id_viaje', # Nombre exacto de la columna FK en tu tabla INVENTARIO
        verbose_name="Viaje Asociado"
    )
    
    # ID_PRODUCTO en DB (Foreign Key), ahora mapeado a 'id_producto' en minúsculas
    id_producto = models.ForeignKey(
        Producto,
        models.PROTECT,
        db_column='id_producto', # Nombre exacto de la columna FK en tu tabla INVENTARIO
        verbose_name="Producto"
    )
    
    # NIVEL_MINIMO en DB, ahora mapeado a 'nivel_minimo' en minúsculas
    nivel_minimo = models.IntegerField(db_column='nivel_minimo', verbose_name="Nivel Mínimo")
    # CANTIDAD_DISPONIBLE en DB, ahora mapeado a 'cantidad_disponible' en minúsculas
    cantidad_disponible = models.IntegerField(db_column='cantidad_disponible', verbose_name="Cantidad Disponible")

    class Meta:
        managed = False
        db_table = 'inventario' # Cambiado a minúsculas
        verbose_name = "Inventario"
        verbose_name_plural = "Inventarios"
        unique_together = (('id_viaje', 'id_producto'),) 
        ordering = ['id_viaje', 'id_producto']

    def __str__(self):
        return f"Inv. Viaje {self.id_viaje.codigo_viaje} - Prod. {self.id_producto.nombre_producto}"