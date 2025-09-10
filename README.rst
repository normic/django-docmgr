======
DocMgr
======
DocMgr is a simple Django app to attach different documents (files) to your
own models.

Features
--------
* Pluggable Document model which can connect Documents to any model
* Templatetag for nice preview of a given (image)document
* Provides DocumentPreviewWidget which shows a preview of an image instead of
  the normal filelink
* When deleting or changing a referenced document, the file will be deleted as well
* Provides a simple AdminModel (not really useful as you would have to enter contenttype by hand)
* Provides predefined AdminInlines (with preview support)


Quick start
-----------

Requirements
############
| django >= 4.2
| django-braces >= 1.4
| django-downloadview >=2.4.0

Prerequisites
#############
The contenttypes framework has to be installed and active. See `Django docs
<https://docs.djangoproject.com/en/5.2/ref/contrib/contenttypes/>`_


Setup
-----

1. Add 'docmgr' to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'docmgr',
    ]

2. Include the docmgr URLconf in your projects urls.py like this::

    path('docmgr/', include('docmgr.urls')),


3. Run `python manage.py migrate` to create the docmgr models.

4. Use docmgr in Admin with your own models::

    from docmgr.models import Document
    from docmgr.admin import DocumentAdmin, DocumentStackedInline, DocumentTabularInline

    class MyDocumentInline(DocumentTabularInline):
        pass

    class MyModelAdmin(DocumentAdmin):
        inlines = [MyDocumentInline]


Settings
########

Define specific setting: ::

  DOCMGR_UPLOAD_PATH = '/home/my_file_path/'

If it's not set in current Django project settings, DocMgr will create a
directory '/files_docmgr/' in your project root.

Hint: The given path doesn't need to be in your MEDIA_ROOT.
