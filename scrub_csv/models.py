from django.db import models


class Uploader(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    is_active = models.BooleanField()

    def __unicode__(self):
        return self.username


class Document(models.Model):
    uploader = models.ForeignKey(Uploader)
    file_name = models.CharField(max_length=200)
    upload_date = models.DateTimeField('date uploaded')

    def __unicode__(self):
        return self.uploader + "-" + self.file_name


class Record(models.Model):
    document = models.ForeignKey(Document)
    row = models.PositiveIntegerField()
    doc_key = models.CharField(max_length=200)
    doc_value = models.CharField(max_length=200, default="")

    def __unicode__(self):
        return self.doc_key + ": " + self.doc_value
