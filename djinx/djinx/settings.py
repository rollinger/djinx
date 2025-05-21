from django.conf import settings

MY_PACKAGE_OPTION = getattr(settings, "MY_PACKAGE_OPTION", "default_value")
