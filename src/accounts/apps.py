from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = "accounts"

    def ready(self):
        from .serializer import UserRegisterSerializer
        from sr_libs.authentication.resource import define_register

        define_register(serializer=UserRegisterSerializer)
