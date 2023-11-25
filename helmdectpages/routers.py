class AuthRouter:
    """
    A router to control all database operations on models in the
    authentication application.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'auth':
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'auth':
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label == 'auth' or
            obj2._meta.app_label == 'auth'
        ):
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'auth':
            return db == 'default'
        return None
