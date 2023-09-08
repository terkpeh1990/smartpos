from django.apps import AppConfig


class AuthAccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_accounts'
    def ready(self):
        import auth_accounts.signals
