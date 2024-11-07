from django.apps import AppConfig


class WeatherProjectConfig(AppConfig):
    """
    Configuration class for teh Weather Project application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather_project'
