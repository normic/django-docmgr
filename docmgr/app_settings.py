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

if not os.path.exists(UPLOAD_PATH):
    os.makedirs(UPLOAD_PATH)
