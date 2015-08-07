from django.db import models

# Create your models here.
class Feature(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    url = models.SlugField()
    img_src = models.ImageField(upload_to='features')
    img_alt = models.CharField(max_length=200)
    def __unicode__(self):
        return unicode(self.title)