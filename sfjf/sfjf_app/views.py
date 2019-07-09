from django.shortcuts import render
from django.template.defaultfilters import slugify
from django.utils import timezone

from . import forms
from . import models

def home(request):
    '''
    Render homepage
    '''
    return render(request, 'base.html')

def edit_post(request, slug=''):
    '''
    Create or edit blog post
    '''
    post = None
    post_info = {}
    if slug != '':
        # Fetch the information for the post we are trying to edit
        post_queryset = models.BlogPostModel.objects.filter(slug=slug)

        post = post_queryset[0] if len(post_queryset) else None
        if post is None:
            raise ValueError('No post identified by slug "{}"'.format(slug))
        else:
            post_info['body'] = post.body

    if request.method == 'POST':
        post_form = forms.BlogPostForm(request.POST, request.FILES)
        if post_form.is_valid():
            # Create slug to uniquely identify this post
            slug = slugify(post_form.cleaned_data['title'])

            # Create info dictionary for this post
            post_info = {
                'title': post_form.cleaned_data['title'],
                'slug': slug,
                'pub_date': timezone.now(),
                'body': post_form.cleaned_data['body'],
            }

            # Save the blog post
            models.BlogPostModel(**post_info).save()
        else:
            raise ValueError('Submitted form is invalid')
    else:
        post_form = forms.BlogPostForm(post_info)

    context = {
        'form': post_form,
    }

    return render(request, 'blog/edit.html', context=context)
