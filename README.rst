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
* When deleting a referenced document, the file will be deleted as well
* Provides an AdminModel


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

3. Use docmgr in your model(s):

   Import GenericRelation and the Document model::
   
    from django.contrib.contenttypes.fields import GenericRelation
    from docmgr.models import Document

   And add a line like this to your model::

    documents = GenericRelation(Document, related_query_name='your_model_name')


Admin integration
-----------------
TODO


Settings
########

Define specific setting: ::

  DOCMGR_UPLOAD_PATH = '/home/my_file_path/'

If it's not set in current Django project settings, DocMgr will create a
directory 'files_docmgr/' in your project root.
