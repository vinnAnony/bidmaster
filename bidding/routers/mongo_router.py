class MongoDBRouter:
    """
    A router to route models to the MongoDB database.
    """

    def db_for_read(self, model, **hints):
        if (
            model._meta.app_label == "bidding"
            and model._meta.model_name == "auctionlog"
        ):
            return "mongodb"
        return None

    def db_for_write(self, model, **hints):
        if (
            model._meta.app_label == "bidding"
            and model._meta.model_name == "auctionlog"
        ):
            return "mongodb"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return None
