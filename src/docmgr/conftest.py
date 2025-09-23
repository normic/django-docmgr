# ... existing code ...
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

import django  # noqa: E402

django.setup()
