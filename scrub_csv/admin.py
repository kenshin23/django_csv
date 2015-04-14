from django.contrib import admin

from .models import Uploader, Document, Record

admin.site.register(Uploader)
admin.site.register(Document)
admin.site.register(Record)
