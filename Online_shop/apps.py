from django.apps import AppConfig


class OnlineShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Online_shop'

    def ready(self):
      import Online_shop.signals
