
class ExternalDBRouter:
    """
    Un enrutador de base de datos que dirige todas las operaciones a la única base de datos 'default'.
    Su principal función es controlar qué aplicaciones pueden aplicar migraciones.
    """
    # Lista de nombres de aplicaciones personalizadas que tienen 'managed=False'
    # y cuyas tablas ya existen en la base de datos 'pruebas'.
    # NO queremos que Django intente generar o aplicar migraciones para estas.
    route_app_labels = {
        'buque_app',
        'viaje_app',
        'inventario_app',
        'productos_app',
        'administrador_app',
        'consumo_app',
        # Si tu app 'login' tiene modelos propios que ya existen en 'pruebas' con 'managed=False',
        # inclúyela aquí. Si 'login' solo usa los modelos de Django (auth, admin) o quieres
        # que Django gestione sus tablas, NO la incluyas aquí.
        # Para esta configuración, la dejamos fuera porque los modelos de 'auth'
        # se gestionarán por el 'else' de allow_migrate.
    }

    def db_for_read(self, model, **hints):
        """
        Todos los modelos leerán de la base de datos 'default'.
        """
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Todos los modelos escribirán en la base de datos 'default'.
        """
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Permite todas las relaciones, ya que todos los modelos están en la misma base de datos.
        """
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Controla qué aplicaciones pueden aplicar migraciones.
        """
        if app_label in self.route_app_labels:
            # Para nuestras apps personalizadas (que tienen managed=False):
            # Devolvemos False para NO permitir que Django genere o aplique migraciones.
            return False
        else:
            # Para todas las demás apps (principalmente las de Django: 'admin', 'auth',
            # 'contenttypes', 'sessions', 'messages', 'staticfiles' y 'login' si tiene modelos propios
            # sin managed=False):
            # Permitimos que Django aplique sus migraciones en la base de datos 'default'.
            return db == 'default'