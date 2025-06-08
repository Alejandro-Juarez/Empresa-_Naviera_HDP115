# buque_app/models.py (VERSIÓN FINAL, LISTA PARA USAR CON TU DB POSTGRESQL EXISTENTE)
from django.db import models

# Modelo TipoBuque: Mapea a la tabla 'tipo_buque' en tu DB PostgreSQL
class TipoBuque(models.Model):
    # La clave primaria 'id_tipo' tal como la detectó inspectdb.
    # Si esta columna es un SERIAL en PostgreSQL, AutoField está bien.
    id_tipo = models.AutoField(db_column='id_tipo', primary_key=True)
    
    # Nombre de la columna en tu DB es 'tipo_buque'
    tipo_buque = models.CharField(db_column='tipo_buque', max_length=15, unique=True) # unique=True añadido para consistencia

    class Meta:
        managed = False  # MUY IMPORTANTE: Le dice a Django que NO cree ni modifique esta tabla.
        db_table = 'tipo_buque' # Nombre EXACTO de la tabla en tu DB PostgreSQL (en minúsculas)
        verbose_name = "Tipo de Buque"
        verbose_name_plural = "Tipos de Buque"

    def __str__(self):
        return self.tipo_buque


# Modelo Buque: Mapea a la tabla 'buque' en tu DB PostgreSQL
class Buque(models.Model):
    # La clave primaria 'id_buque' tal como la detectó inspectdb.
    id_buque = models.AutoField(db_column='id_buque', primary_key=True)

    # id_tipo es el nombre de la columna FK en tu tabla 'buque'
    # 'to' apunta a la clase TipoBuque que acabamos de definir
    # on_delete=models.PROTECT: Para evitar eliminar un TipoBuque si hay Buques asociados
    tipo_buque = models.ForeignKey(
        TipoBuque,
        models.PROTECT, # Cambiado de DO_NOTHING a PROTECT
        db_column='id_tipo', # Este es el nombre de la columna en tu tabla 'buque' que es la FK
        verbose_name="Tipo de Buque",
        related_name='buques_asociados' # Nombre para acceder desde TipoBuque (ej. tipo.buques_asociados.all())
    )
    
    # nombre_buque es el nombre de la columna en tu DB. Lo mapeamos a 'nombre' en el modelo.
    nombre = models.CharField(db_column='nombre_buque', max_length=100, verbose_name="Nombre del Buque") # Max_length ajustado a 100
    
    # matricula es el nombre de la columna en tu DB. unique=True añadido para consistencia.
    matricula = models.CharField(db_column='matricula', max_length=50, unique=True, verbose_name="Matrícula") # Max_length ajustado a 50
    
    # capacidad es el nombre de la columna en tu DB. Lo mapeamos a 'capacidad_toneladas'.
    capacidad_toneladas = models.FloatField(db_column='capacidad', verbose_name="Capacidad (Toneldas)")

    class Meta:
        managed = False  # MUY IMPORTANTE: Le dice a Django que NO cree ni modifique esta tabla.
        db_table = 'buque' # Nombre EXACTO de la tabla en tu DB PostgreSQL (en minúsculas)
        verbose_name = "Buque"
        verbose_name_plural = "Buques"
        ordering = ['nombre'] # Opcional: ordenar por nombre por defecto

    def __str__(self):
        return f"{self.nombre} ({self.matricula})"


# --- Otros modelos generados por inspectdb que NO vamos a modificar en esta aplicación ---
# Puedes dejarlos en este archivo models.py si tu aplicación los necesita en el futuro,
# pero para la app de gestión de buques, solo nos centramos en Buque y TipoBuque.
# Si solo vas a usar Buque y TipoBuque, podrías eliminar el resto de estas clases
# para mantener tu models.py más limpio y centrado.

class CategoriaProducto(models.Model):
    id_categoria = models.AutoField(db_column='id_categoria', primary_key=True)
    nombre_categoria = models.CharField(db_column='nombre_categoria', max_length=10) # Max_length 10 es muy corto para nombres

    class Meta:
        managed = False
        db_table = 'categoria_producto'
        verbose_name = "Categoría de Producto"
        verbose_name_plural = "Categorías de Producto"
    def __str__(self): return self.nombre_categoria

class EstadoViaje(models.Model):
    id_estado = models.AutoField(db_column='id_estado', primary_key=True)
    estado_viaje = models.CharField(db_column='estado_viaje', max_length=20)

    class Meta:
        managed = False
        db_table = 'estado_viaje'
        verbose_name = "Estado de Viaje"
        verbose_name_plural = "Estados de Viaje"
    def __str__(self): return self.estado_viaje

class Inventario(models.Model):
    id_inventario = models.AutoField(db_column='id_inventario', primary_key=True)
    id_producto = models.ForeignKey('Producto', models.DO_NOTHING, db_column='id_producto')
    nivel_minimo = models.IntegerField(db_column='nivel_minimo')
    cantidad_disponible = models.IntegerField(db_column='cantidad_disponible')

    class Meta:
        managed = False
        db_table = 'inventario'
        verbose_name = "Inventario"
        verbose_name_plural = "Inventario"
    def __str__(self): return f"Inv {self.id_inventario}" # O un campo más descriptivo


class Producto(models.Model):
    id_producto = models.AutoField(db_column='id_producto', primary_key=True)
    id_unidad_medida = models.ForeignKey('UnidadMedida', models.DO_NOTHING, db_column='id_unidad_medida')
    id_categoria = models.ForeignKey(CategoriaProducto, models.DO_NOTHING, db_column='id_categoria')
    nombre_producto = models.CharField(db_column='nombre_producto', max_length=20) # Max_length 20 es corto

    class Meta:
        managed = False
        db_table = 'producto'
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
    def __str__(self): return self.nombre_producto


class UnidadMedida(models.Model):
    id_unidad_medida = models.AutoField(db_column='id_unidad_medida', primary_key=True)
    nombre_unidad_medida = models.CharField(db_column='nombre_unidad_medida', max_length=20)

    class Meta:
        managed = False
        db_table = 'unidad_medida'
        verbose_name = "Unidad de Medida"
        verbose_name_plural = "Unidades de Medida"
    def __str__(self): return self.nombre_unidad_medida


class Viaje(models.Model):
    id_viaje = models.AutoField(db_column='id_viaje', primary_key=True)
    id_estado = models.ForeignKey(EstadoViaje, models.DO_NOTHING, db_column='id_estado')
    id_inventario = models.ForeignKey(Inventario, models.DO_NOTHING, db_column='id_inventario')
    id_buque = models.ForeignKey(Buque, models.DO_NOTHING, db_column='id_buque')
    codigo_viaje = models.IntegerField(db_column='codigo_viaje')
    fecha_inicio = models.DateField(db_column='fecha_inicio')
    fecha_fin = models.DateField(db_column='fecha_fin')
    destino = models.CharField(db_column='destino', max_length=50)

    class Meta:
        managed = False
        db_table = 'viaje'
        verbose_name = "Viaje"
        verbose_name_plural = "Viajes"
    def __str__(self): return f"Viaje {self.codigo_viaje}"