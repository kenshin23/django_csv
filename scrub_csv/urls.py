from django.conf.urls import url

from . import views

urlpatterns = [
    # File processing views:
    # ex: /files/
    url(r'^$', views.index, name='index'),

    # ex: /files/new/ -- This lets the user upload a file
    url(r'^new/$', views.new, name='new'),

    # ex: /files/5/ -- This lets the user see relevant file info
    url(r'^(?P<document_id>[0-9]+)/$',
        views.detail, name='detail'),

    # ex: /files/5/select/ -- This lets the user map file headers
    # to database fields
    url(r'^(?P<document_id>[0-9]+)/select/$',
        views.select_fields, name='select_fields'),

    # ex: /files/5/process/ -- This processes the file and imports
    # the records to the database
    url(r'^(?P<document_id>[0-9]+)/process/$',
        views.process, name='process'),

    # ex: /files/5/scrub/ -- This returns the scrubbing result for 
    # the uploaded file, cleaning up if necessary.
    url(r'^(?P<document_id>[0-9]+)/scrub/$',
        views.scrub, name='scrub'),

    # ex: /files/5/records/ -- This shows the processing result
    url(r'^(?P<document_id>[0-9]+)/records/$',
        views.records, name='records'),
]
