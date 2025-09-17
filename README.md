# django-docmgr

> *A small, pluggable Django app to store and reference uploaded documents (files) from any model.*

This release expands the project with optional Django REST Framework (DRF) integration so it can be
used comfortably in API-centric projects without relying solely on Django Admin. The DRF layer is
secure by default and simple to wire into existing routers.

## Features
- Django Admin integration with preview of uploaded files.
- Document model with robust, slugified upload paths and configurable directory structure.
- Generic relation support: attach a document to any model via ContentType + object_id.
- Classic Django views for thumbnail/default file via django-downloadview.
- Optional DRF module (serializer + viewset) providing secure CRUD + download endpoints.

## Requirements
- Python 3.10+
- Django 4.2+
- django-braces (>=1.4 recommended)
- django-downloadview (>=2.4.0 recommended)
- Optional: djangorestframework (if you use the API integration)

### Prerequisites
- Ensure Django’s contenttypes framework is installed and active.
  See https://docs.djangoproject.com/en/5.2/ref/contrib/contenttypes/

---

## Installation
1) Install the package:
`   pip install django-docmgr
`

2) Add the app to INSTALLED_APPS:
```
   INSTALLED_APPS = [
       ...,
       "docmgr",
       # Optional if you use DRF integration
       # "rest_framework",
   ]
```

### Admin quick start (Django Admin)
1) Include the classic URLconf (optional, only if you use the provided views):
   path("docmgr/", include("docmgr.urls")),

2) Use docmgr in your Admin with predefined inlines (includes image preview support):
```
   from docmgr.models import Document
   from docmgr.admin import DocumentAdmin, DocumentStackedInline, DocumentTabularInline

   class MyDocumentInline(DocumentTabularInline):
       pass

   class MyModelAdmin(DocumentAdmin):
       inlines = [MyDocumentInline]
```

### Settings
#### Minimal settings (all optional):
- DOCMGR_UPLOAD_PATH: Base directory where files are stored (default: BASE_DIR / "files_docmgr").
  If not set, DocMgr will create a "files_docmgr" directory in your project root. The given path
  does not need to live under MEDIA_ROOT.
- DOCMGR_UPLOAD_STRUCTURE: Subdirectory structure under the base path. One of:
  - "year" (default) -> YYYY/
  - "year_month" -> YYYY/MM/
  - "date" or "date_iso" -> YYYY-MM-DD/

#### DRF-related optional settings:
- DOCMGR_DRF_PERMISSION_CLASSES: list[str]
  Defaults to [
    "rest_framework.permissions.IsAuthenticated",
    "rest_framework.permissions.DjangoModelPermissions",
  ]. 
 Provide dotted paths to DRF permission classes you want to enforce on the viewset.

- DOCMGR_DRF_THROTTLE_SCOPE: str
  Defaults to "docmgr". Used with DRF's ScopedRateThrottle.


## Quick start (DRF)
1) Install DRF if you haven't:
   pip install djangorestframework

2) Add rest_framework to INSTALLED_APPS.

3) Wire the viewset to your router (urls.py):
```
   from django.urls import path, include
   from rest_framework.routers import DefaultRouter
   from docmgr.drf import DocumentViewSet

   router = DefaultRouter()
   router.register(r"documents", DocumentViewSet, basename="document")

   urlpatterns = [
       path("api/", include(router.urls)),
   ]
```

4) Ensure model permissions are in place. By default, the API requires authentication and Django model permissions (view/add/change/delete) for docmgr.Document. Grant users/groups the appropriate perms in your auth backend or via migrations/fixtures.


## API reference (DRF)
Base path below assumes /api/documents/.
- List: GET /api/documents/
  Optional filtering by related object:
    ?content_type=<id|app_label.model>&object_id=<int>

- Retrieve: GET /api/documents/{uuid}/

- Create (upload): POST /api/documents/
  Content-Type: multipart/form-data
  Fields:
    - docfile: file (required)
    - description: string (optional)
    - content_type: integer id OR "app_label.model" (optional)
    - object_id: integer (optional)

- Update: PUT/PATCH /api/documents/{uuid}/
  You can update description, and optionally re-upload docfile.

- Delete: DELETE /api/documents/{uuid}/

- Download file contents: GET /api/documents/{uuid}/download/?attachment=1
  If attachment=0/false, most browsers will try to display inline.

### Attaching documents to your models
You can link a Document to any model using content_type + object_id (GenericForeignKey):
- On upload, pass content_type and object_id.
  Example content_type values:
   - 9 (ContentType pk)
   - "blog.post" (app_label.model in lowercase)

- To list all documents for a specific object:
  GET /api/documents/?content_type=blog.post&object_id=123

#### Permissions and throttling
- Permissions default to IsAuthenticated + DjangoModelPermissions.
- Throttling is opt-in. DocumentViewSet only enables throttling if your DRF settings define a rate for the configured scope (DOCMGR_DRF_THROTTLE_SCOPE, default "docmgr") in DEFAULT_THROTTLE_RATES. If no rate is present, throttling is disabled and no error is raised.

#### Customizing permissions
Provide your own permission classes via settings:
```
DOCMGR_DRF_PERMISSION_CLASSES = [
  "rest_framework.permissions.IsAuthenticated",
  "rest_framework.permissions.DjangoModelPermissions",
  # Example: "yourapp.permissions.OwnerOrReadOnly"
]
```

#### Enabling throttling (optional)
```
REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.ScopedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "docmgr": "50/min",
    },
}
```
Note on "No default throttle rate set for 'docmgr' scope"
If you enable ScopedRateThrottle but forget to add a rate for the "docmgr" scope in DEFAULT_THROTTLE_RATES, 
DRF will normally raise that error. The viewset avoids this by activating throttling only when a rate exists.
To throttle docmgr endpoints, add the rate as shown above.

### Security considerations and best practices
- Keep DOCMGR_UPLOAD_PATH outside STATIC_ROOT and ensure your web server does not serve it publicly without 
  authentication.
- Rely on Django/DRF permissions to protect listing, retrieving, and downloading of documents.
- Use throttling to prevent abusive uploads/downloads.
- Filenames are slugified; upload subfolders are controlled by DOCMGR_UPLOAD_STRUCTURE to avoid traversal issues.
- For production downloads, consider serving via django-downloadview or signed URLs if needed. The DRF download 
  action uses FileResponse and honors permissions.


## Examples

curl upload (attach to object blog.post #123):
>  curl -X POST \
    -H "Authorization: Bearer <token>" \
    -F "docfile=@/path/to/photo.jpg" \
    -F "description=A sample file" \
    -F "content_type=blog.post" \
    -F "object_id=123" \
    http://localhost:8000/api/documents/

---

curl list for given object:
>  curl -H "Authorization: Bearer <token>" \
    "http://localhost:8000/api/documents/?content_type=blog.post&object_id=123"

---

curl download inline:
>  curl -L -H "Authorization: Bearer <token>" \
    "http://localhost:8000/api/documents/<uuid>/download/?attachment=0" -o -

---
Python (requests) upload:
```  import requests
  files = {"docfile": open("/path/file.pdf", "rb")}
  data = {"description": "My doc", "content_type": "shop.order", "object_id": 42}
  r = requests.post("http://localhost:8000/api/documents/", files=files, data=data, headers={"Authorization": "Bearer <token>"})
  r.raise_for_status()
  print(r.json())
```


## FAQ
- _Is DRF required?_ No. docmgr works without DRF. The DRF integration lives in docmgr.drf and is only imported if you use it.
- _Can I store files in cloud storage?_ Yes. Configure DEFAULT_FILE_STORAGE or provide a custom storage in your 
  project; docmgr uses a FileField and respects Django's storage backends.
- _How do I restrict access so users see only their own files?_ Provide a custom permission and/or override 
  get_queryset in your own subclass of DocumentViewSet.

