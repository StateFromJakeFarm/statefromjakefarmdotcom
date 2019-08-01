from random import shuffle

from . import models

def get_post(slug):
    '''
    Return the post identified by a given slug, or None if none exists
    '''
    post_queryset = models.BlogPostModel.objects.filter(slug=slug)

    return (post_queryset[0] if len(post_queryset) else None)
