from django.contrib import admin

from .models import Uploader, Document, Row, Record

admin.site.register(Uploader)


class DocumentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                   {'fields': ['csvfile']}),
        ('Uploader information', {'fields': ['uploader']})
    ]
    list_display = ('csvfile', 'uploader', 'upload_date')


admin.site.register(Document, DocumentAdmin)

admin.site.register(Row)

admin.site.register(Record)
