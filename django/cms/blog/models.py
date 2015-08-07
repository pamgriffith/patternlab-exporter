from django.db import models
from markupfield.fields import MarkupField

from django.utils import timezone

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=200)
    url = models.SlugField()
    excerpt = MarkupField(markup_type='markdown')
    content = MarkupField(markup_type='markdown')
    date = models.DateTimeField(default=timezone.now)
    def __unicode__(self):
        return unicode(self.title)