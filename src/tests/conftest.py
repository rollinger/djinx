import django
from django.conf import settings

# Configure Django only once
if not settings.configured:
    settings.configure(
        SECRET_KEY="dummy-secret-for-testing",
        ROOT_URLCONF="hello",  # will be overridden per test if needed
        INSTALLED_APPS=[
            # Add any app that may be required (e.g., if your views use templates)
            # but often none are needed for routing tests.
        ],
        # If you use the test client, you might need MIDDLEWARE (optional)
        MIDDLEWARE=[],  # empty for speed
    )
    django.setup()
