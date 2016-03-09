# app specific settings
import os

from django.conf import settings

UPLOAD_PATH = getattr(settings, 'DOCMGR_UPLOAD_PATH', 'docmgr/')

MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', settings.BASE_DIR + '/files/')


if not os.path.exists(os.path.join(MEDIA_ROOT, UPLOAD_PATH)):
    os.makedirs(os.path.join(MEDIA_ROOT, UPLOAD_PATH))
