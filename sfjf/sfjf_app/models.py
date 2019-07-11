from django.db import models
from markdownx.models import MarkdownxField

class BlogPostModel(models.Model):
    '''
    Store information associated with blog post
    '''
    title = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    preview = models.CharField(max_length=128)
    pub_date = models.DateTimeField()
    body = MarkdownxField()
