from django.conf.urls import url

from . import views

urlpatterns = [
    # File processing views:
    # ex: /files/3/ -- This shows the files uploaded by Uploader id 3
    url(r'^(?P<uploader_id>[0-9]+)/$', views.index, name='index'),

    # ex: /files/3/new/ -- This lets the user upload a file
    url(r'^(?P<uploader_id>[0-9]+)/new/$', views.new, name='new'),

    # ex: /files/3/5/ -- This lets the user see relevant file info
    url(r'^(?P<uploader_id>[0-9]+)/(?P<document_id>[0-9]+)/$',
        views.detail, name='detail'),

    # ex: /files/3/5/select/ -- This lets the user map file headers
    # to database fields
    url(r'^(?P<uploader_id>[0-9]+)/(?P<document_id>[0-9]+)/select/$',
        views.select_fields, name='select_fields'),

    # ex: /files/3/5/process/ -- This processes the file and imports
    # the records to the database
    url(r'^(?P<uploader_id>[0-9]+)/(?P<document_id>[0-9]+)/process/$',
        views.process, name='process'),

    # ex: /files/3/5/scrub/import_only -- This returns the scrubbing result for
    # the uploaded file, cleaning up if necessary
    url(r'^(?P<uploader_id>[0-9]+)/(?P<document_id>[0-9]+)'
        r'/scrub/(?P<action>\w+)/$', views.scrub, name='scrub'),

    # ex: /files/3/5/download/ -- This downloads the corresponding generated
    # results file
    url(r'^(?P<uploader_id>[0-9]+)/(?P<document_id>[0-9]+)'
        r'/download/(?P<file_type>\w+)/$', views.download, name='download'),

    # ex: /files/5/records/ -- This shows the processing result
    url(r'^(?P<uploader_id>[0-9]+)/(?P<document_id>[0-9]+)/records/$',
        views.records, name='records'),
]
