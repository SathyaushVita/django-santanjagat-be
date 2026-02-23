# class RegisterRouter:
#     """
#     A router to control all database operations on models in the
#     Login model.
#     """

#     def db_for_read(self, model, **hints):
#         """
#         Attempts to read Login models go to gramadevata_updated.
#         """
#         if model.__name__ == 'Register':
#             return 'gramadevata_updated'
#         return 'default'

#     def db_for_write(self, model, **hints):
#         """
#         Attempts to write Login models go to gramadevata_updated.
#         """
#         if model.__name__ == 'Register':
#             return 'gramadevata_updated'
#         return 'default'

#     def allow_relation(self, obj1, obj2, **hints):
#         """
#         Allow relations if a model in the Login model is involved.
#         """
#         if obj1.__class__.__name__ == 'Register' or obj2.__class__.__name__ == 'Register':
#             return True
#         return None

#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         """
#         Make sure the Login model only appears in the 'gramadevata_updated' database.
#         """
#         if model_name == 'Register':
#             return db == 'gramadevata_updated'
#         return db == 'default'







class RegisterRouter:
    """
    A router to control all database operations on models in the Register, Event, EventCategory, and Comment models.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read Register, Event, EventCategory, and Comment models go to gramadevata_updated1.
        """
        if model.__name__ in ['Register', 'Event', 'EventCategory', 'CommentModel']:
            return 'gramadevata_updated1'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Attempts to write Register, Event, EventCategory, and Comment models go to gramadevata_updated1.
        """
        if model.__name__ in ['Register', 'Event', 'EventCategory', 'CommentModel']:
            return 'gramadevata_updated1'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the Register, Event, EventCategory, or Comment model is involved.
        """
        if (obj1.__class__.__name__ in ['Register', 'Event', 'EventCategory', 'CommentModel'] or
                obj2.__class__.__name__ in ['Register', 'Event', 'EventCategory', 'CommentModel']):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the Register, Event, EventCategory, and Comment models only appear in the 'gramadevata_updated1' database.
        """
        if model_name in ['Register', 'Event', 'EventCategory', 'CommentModel']:
            return db == 'gramadevata_updated1'
        return db == 'default'
