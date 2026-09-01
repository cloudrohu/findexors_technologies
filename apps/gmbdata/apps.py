from django.apps import AppConfig


class GmbdataConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"

    name = 'apps.gmbdata'
    verbose_name = "GMB Data"




from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.blog"
    verbose_name = "Blog"
