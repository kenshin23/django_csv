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


class RecordAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Record information', {'fields': [
            'row', 'doc_key', 'doc_value']})
    ]
    list_display = ('get_row', 'doc_key', 'doc_value')

    def get_row(self, obj):
        return obj.row.id
    get_row.short_description = 'Row #'
    get_row.admin_order_field = 'row__id'

admin.site.register(Record, RecordAdmin)
