from django.db import models

# Create your models here.
class Hero(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    cta_link = models.URLField()
    cta_text = models.CharField(max_length=200)
    def __unicode__(self):
        return unicode(self.title)