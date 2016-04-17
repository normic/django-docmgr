# app specific settings
import os

from django.conf import settings

UPLOAD_PATH = getattr(settings, 'DOCMGR_UPLOAD_PATH', settings.BASE_DIR + '/files_docmgr/')

if not os.path.exists(UPLOAD_PATH):
    os.makedirs(UPLOAD_PATH)
