# app specific settings
import os
from pathlib import Path

from django.conf import settings

default_path = (
    (Path(settings.BASE_DIR) / "files_docmgr")
    if hasattr(settings, "BASE_DIR")
    else "files_docmgr"
)
UPLOAD_PATH = getattr(settings, "DOCMGR_UPLOAD_PATH", str(default_path))

# Controls how uploaded files are placed into subdirectories under UPLOAD_PATH.
# Allowed values:
#   - "year" (default): YYYY/
#   - "year_month": YYYY/MM/
#   - "date" or "date_iso": YYYY-MM-DD/
UPLOAD_STRUCTURE = getattr(settings, "DOCMGR_UPLOAD_STRUCTURE", "year")

# DRF integration (optional). You can override these in your Django settings.
# - DOCMGR_DRF_PERMISSION_CLASSES: list of dotted paths to DRF permission classes.
#   Defaults to ["rest_framework.permissions.IsAuthenticated", "rest_framework.permissions.DjangoModelPermissions"].
# - DOCMGR_DRF_THROTTLE_SCOPE: scope name to use with ScopedRateThrottle (e.g., "docmgr").
DOCMGR_DRF_PERMISSION_CLASSES = getattr(
    settings,
    "DOCMGR_DRF_PERMISSION_CLASSES",
    [
        "rest_framework.permissions.IsAuthenticated",
        "rest_framework.permissions.DjangoModelPermissions",
    ],
)
DOCMGR_DRF_THROTTLE_SCOPE = getattr(settings, "DOCMGR_DRF_THROTTLE_SCOPE", "docmgr")

if not os.path.exists(UPLOAD_PATH):
    os.makedirs(UPLOAD_PATH)
