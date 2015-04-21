from django.db import models
from django.contrib.auth.models import User


# A user is an uploader as well.
class Uploader(models.Model):
    user = models.OneToOneField(User)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.user.username


# A user can upload many documents...
class Document(models.Model):
    uploader = models.ForeignKey(Uploader)
    csvfile = models.FileField(upload_to='uploads/%Y/%m/%d',
                               verbose_name='file')
    found_file = models.FileField(upload_to='uploads/%Y/%m/%d',
                                  verbose_name='found records',
                                  blank=True, null=True)
    not_found_file = models.FileField(upload_to='uploads/%Y/%m/%d',
                                      verbose_name='not found records',
                                      blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True,
                                       verbose_name="date uploaded")

    def __unicode__(self):
        timeformat = "%Y%m%d_%H%M%S"
        return u'%s_%s' % (str(self.uploader.id),
                           self.upload_date.strftime(timeformat))


# ...A document can have many rows (which can be permanent or just
# to scrub against, then deleted afterwards)...
class Row(models.Model):
    document = models.ForeignKey(Document)
    permanent = models.BooleanField(default=True)

    def __unicode__(self):
        return str(self.document.id) + ": " + str(self.id)


# ...and a row can have many records (key:value)
class Record(models.Model):
    row = models.ForeignKey(Row)
    doc_key = models.CharField(max_length=200)
    doc_value = models.CharField(max_length=200, default="")

    def __unicode__(self):
        return self.doc_key + ": " + self.doc_value
