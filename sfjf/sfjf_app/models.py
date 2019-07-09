from django.db import models
from markdownx.models import MarkdownxField

class BlogPostModel(models.Model):
    '''
    Store information associated with blog post
    '''
    title = models.CharField(max_length=256)
    pub_date = models.DateTimeField()
    image = models.ImageField(upload_to='images/')
    body = MarkdownxField()
