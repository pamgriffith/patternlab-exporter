from django.db import models

from django.utils import timezone

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=200)
    url = models.SlugField()
    excerpt = models.TextField()
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    def __unicode__(self):
        return unicode(self.title)