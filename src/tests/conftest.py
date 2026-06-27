import django
from pathlib import Path
from django.conf import settings

TEST_DIR = Path(__file__).parent
TEMPLATE_DIR = str(TEST_DIR / "data")  # absolute string path usable by Django

# Configure Django only once
if not settings.configured:
    settings.configure(
        SECRET_KEY="dummy-secret-for-testing",
        ROOT_URLCONF=__name__,  # will be overridden per test if needed
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "djxi",
        ],
        MIDDLEWARE=[],  # empty for speed
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [TEMPLATE_DIR],
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
