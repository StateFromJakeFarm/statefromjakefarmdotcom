from random import shuffle

from . import models

def get_post(slug):
    '''
    Return the post identified by a given slug, or None if none exists
    '''
    post_queryset = models.BlogPostModel.objects.filter(slug=slug)

    return (post_queryset[0] if len(post_queryset) else None)

def randomize_home_text(name=['State', 'From', 'Jake', 'Farm']):
    '''
    Return randomized version of site title for comedic effect
    '''
    new_name = name[:]
    shuffle(new_name)

    if new_name == ['Jake', 'From', 'State', 'Farm']:
        # I don't want any legal trouble
        return ''.join(name)

    return ''.join(new_name)
