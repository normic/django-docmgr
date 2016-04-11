======
DocMgr
======
DocMgr is a simple Django app to attach different documents (files) to your
own models.

Features
--------
* Pluggable Document which can connect Documents to any model
* Templatetag for nice preview of a given (image)document
* Provides DocuemntPreviewWidget which shows a preview of an image instead of
  the normal filelink
* When deleting or changing a referenced document, the file will be deleted as well
* Provides a simple AdminModel


Quick start
-----------

Requirements
############
django >= 1.8
django-braces >= 1.4

Prerequisites
#############
The contenttypes framework has to be installed and active. See `Django docs
<https://docs.djangoproject.com/en/1.8/ref/contrib/contenttypes/>`_


Setup
-----

1. Add 'docmgr' to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'docmgr',
    ]

2. Run `python manage.py migrate` to create the docmgr models.

3. Use docmgr in Admin with your own models::

    from docmgr.models import Document
    from docmgr.admin import DocumentAdmin, DocumentStackedInline, DocumentTabularInline

    class MyDocumentInline(DocumentTabularInline):
        extra = 1

    class MyModelAdmin(DocumentAdmin):
        inlines = [MyDocumentInline]


Settings
########

Define specific setting: ::

  DOCMGR_UPLOAD_PATH = '/home/my_file_path/'

If it's not set in current Django project settings, DocMgr will create a
directory 'files_docmgr/' in your project root.

Check if you've set MEDIA_ROOT to some reasonable value.
