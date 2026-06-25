# python
import django
from django.conf import settings

# Configure Django only once
if not settings.configured:
    settings.configure(
        SECRET_KEY="dummy-secret-for-testing",
        ROOT_URLCONF=__name__,  # will be overridden per test if needed
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
        ],
        MIDDLEWARE=[],  # empty for speed
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [],
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": [
                        "django.template.context_processors.request",
                    ],
                },
            }
        ],
    )
    django.setup()
