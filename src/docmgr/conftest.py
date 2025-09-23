import os
from pathlib import Path

from django.conf import settings

if not settings.configured:
    BASE_DIR = Path.cwd()
    settings.configure(
        SECRET_KEY="test-secret-key",
        DEBUG=True,
        BASE_DIR=BASE_DIR,
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.admin",
            "docmgr",
        ],
        MIDDLEWARE=[
            "django.middleware.security.SecurityMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
        ],
        ROOT_URLCONF="docmgr.urls",
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [],
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": [
                        "django.template.context_processors.debug",
                        "django.template.context_processors.request",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                    ],
                },
            }
        ],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": str(BASE_DIR / "db.sqlite3"),
            }
        },
        USE_TZ=True,
        TIME_ZONE="UTC",
        STATIC_URL="static/",
        DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
        # Ensure app_settings chooses a writable path for test files
        DOCMGR_UPLOAD_PATH=str(BASE_DIR / "files_docmgr"),
    )

# Create upload directory proactively for tests
os.makedirs(settings.DOCMGR_UPLOAD_PATH, exist_ok=True)

import django  # noqa: E402

django.setup()


# Ensure Django test environment + test DBs are created for pytest runs
import pytest  # noqa: E402
from django.test.utils import (  # noqa: E402
    setup_test_environment,
    teardown_test_environment,
    setup_databases,
    teardown_databases,
)


@pytest.fixture(scope="session", autouse=True)
def _django_test_environment_and_db():
    # Prepare Django's testing environment (e.g., clears caches, sets DEBUG flags)
    setup_test_environment()
    # Create test databases (runs migrations)
    db_cfg = setup_databases(verbosity=0, interactive=False, keepdb=False)
    try:
        yield
    finally:
        # Drop test databases and restore environment
        teardown_databases(db_cfg, verbosity=0)
        teardown_test_environment()
