from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    name = 'profiles'

    def ready(self):
        import profiles.signals

# we need to add this ProfilesConfig to our __init__.py files as well
