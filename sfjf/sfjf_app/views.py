from django.shortcuts import render
from django.template.defaultfilters import slugify
from django.utils import timezone
from markdown import markdown

from . import forms
from . import models
from . import helpers

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
        post = helpers.get_post(slug)
        if post is None:
            raise ValueError('No post identified by slug "{}"'.format(slug))
        else:
            # Use existing title and body for this post
            post_info['title'] = post.title
            post_info['body'] = post.body

    if request.method == 'POST':
        # Process submitted form
        post_form = forms.BlogPostForm(request.POST, request.FILES)
        if post_form.is_valid():
            if post is None:
                # Save new blog post
                post_info = {
                    'title': title,
                    'slug': slug,
                    'pub_date': timezone.now(),
                    'body': post_form.cleaned_data['body'],
                }

                models.BlogPostModel(**post_info).save()
            else:
                # Update only the body and publication date for existing blog
                # post
                post.body = post_form.cleaned_data['body']
                post.pub_date = timezone.now()

                post.save(update_fields=['pub_date', 'body'])
        else:
            raise ValueError('Submitted form is invalid')
    else:
        # Display form
        post_form = forms.BlogPostForm(post_info)
        if post is not None:
            # Don't let user modify title (because I don't want to change the
            # post's slug right now)
            post_form.fields['title'].widget.attrs['readonly'] = True

    context = {
        'form': post_form,
    }

    return render(request, 'blog/edit.html', context=context)


def view_post(request, slug=''):
    '''
    View an entire blog post
    '''
    # Fetch the information for the post we are trying to edit
    post = helpers.get_post(slug)
    if post is None:
        raise ValueError('No post identified by slug "{}"'.format(slug))

    context = {
        'post': post,
        'body': markdown(post.body),
    }

    return render(request, 'blog/view.html', context=context)
