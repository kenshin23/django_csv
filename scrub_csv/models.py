from django.db import models
from django.contrib.auth.models import User


class Uploader(models.Model):
    user = models.OneToOneField(User)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.user.username


class Document(models.Model):
    uploader = models.ForeignKey(Uploader)
    csvfile = models.FileField(upload_to='uploads/%Y/%m/%d')
    upload_date = models.DateTimeField('date uploaded')

    # def __unicode__(self):
    # FIXME: convert upload_date to string.
    #     return "%s_%s", str(self.uploader.id), self.upload_date


class Record(models.Model):
    document = models.ForeignKey(Document)
    row = models.PositiveIntegerField()
    doc_key = models.CharField(max_length=200)
    doc_value = models.CharField(max_length=200, default="")

    def __unicode__(self):
        return self.doc_key + ": " + self.doc_value
