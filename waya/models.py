from django.db import models

# Create your models here.
class Data(models.Model):
    datatype = models.CharField(max_length = 30)
    database = models.FileField(upload_to = './upload/')

    def __unicode__(self):
        return self.username
