from django.db import models

# Create your models here.
from django.db import models

class TipoBuque(models.Model):
    tipo_buque = models.CharField(max_length=20)

    class Meta:
        db_table = 'tipo_buque'

class Buque(models.Model):
    tipo = models.ForeignKey(TipoBuque, on_delete=models.RESTRICT, db_column='id_tipo')
    nombre_buque = models.CharField(max_length=50)
    matricula = models.CharField(max_length=10)
    capacidad = models.FloatField()

    class Meta:
        db_table = 'buque'

class CategoriaProducto(models.Model):
    id_categoria = models.AutoField(primary_key=True, db_column='id_categoria')
    nombre_categoria = models.CharField(max_length=20, db_column='nombre_categoria')

    class Meta:
        db_table = 'categoria_producto'
        managed = False

    def __str__(self):
        return self.nombre_categoria
    
class UnidadMedida(models.Model):
    nombre_unidad_medida = models.CharField(max_length=20)

    class Meta:
        db_table = 'unidad_medida'

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True, db_column='id_producto')
    id_unidad_medida = models.ForeignKey('UnidadMedida', on_delete=models.RESTRICT, db_column='id_unidad_medida')
    id_categoria = models.ForeignKey('CategoriaProducto', on_delete=models.RESTRICT, db_column='id_categoria')
    nombre_producto = models.CharField(max_length=20, db_column='nombre_producto')
    url_foto = models.CharField(max_length=500, db_column='url_foto')

    class Meta:
        db_table = 'producto'
        managed = False

    def __str__(self):
        return self.nombre_producto

class EstadoViaje(models.Model):
    id_estado = models.AutoField(primary_key=True, db_column='id_estado')
    estado_viaje = models.CharField(max_length=20)

    class Meta:
        db_table = 'estado_viaje'

class Viaje(models.Model):
    id_viaje = models.AutoField(primary_key=True, db_column='id_viaje')
    estado = models.ForeignKey('EstadoViaje', on_delete=models.RESTRICT, db_column='id_estado')
    buque = models.ForeignKey('Buque', on_delete=models.RESTRICT, db_column='id_buque')
    codigo_viaje = models.IntegerField(db_column='codigo_viaje')
    fecha_inicio = models.DateField(db_column='fecha_inicio')
    fecha_fin = models.DateField(db_column='fecha_fin')
    destino = models.CharField(max_length=50, db_column='destino')

    class Meta:
        db_table = 'viaje'
        managed = False

    def __str__(self):
        return f"Viaje {self.codigo_viaje} - {self.destino}"
    
class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True, db_column='id_inventario')
    id_viaje = models.ForeignKey('Viaje', on_delete=models.RESTRICT, db_column='id_viaje')
    id_producto = models.ForeignKey('Producto', on_delete=models.RESTRICT, db_column='id_producto')
    nivel_minimo = models.IntegerField(db_column='nivel_minimo')
    cantidad_disponible = models.IntegerField(db_column='cantidad_disponible')

    class Meta:
        db_table = 'inventario'
        managed = False

    @property
    def categoria(self):
        return self.id_producto.id_categoria.nombre_categoria if self.id_producto else ""

    @property
    def nombre_producto(self):
        return self.id_producto.nombre_producto if self.id_producto else ""

    @property
    def foto(self):
        return self.id_producto.url_foto if self.id_producto else ""
