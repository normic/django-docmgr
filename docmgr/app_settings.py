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

if not os.path.exists(UPLOAD_PATH):
    os.makedirs(UPLOAD_PATH)
