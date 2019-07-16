from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from markdown import markdown
from os.path import join

from . import forms
from . import models
from . import helpers

def home(request):
    '''
    Render homepage
    '''
    context = {
        'home_text': helpers.randomize_home_text(),
    }

    return render(request, 'base.html', context=context)


@login_required
@permission_required('user.is_staff', raise_exception=True)
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
            post_info['preview'] = post.preview
            post_info['body'] = post.body

    if request.method == 'POST':
        # Process submitted form
        post_form = forms.BlogPostForm(request.POST, request.FILES)
        if post_form.is_valid():
            if post is None:
                # Save new blog post
                slug = slugify(post_form.cleaned_data['title'])
                post_info = {
                    'title': post_form.cleaned_data['title'],
                    'slug': slug,
                    'pub_date': timezone.now(),
                    'preview': post_form.cleaned_data['preview'],
                    'body': post_form.cleaned_data['body'],
                }

                models.BlogPostModel(**post_info).save()
            else:
                # Update only body, preview and publication date for
                # existing post
                post.preview = post_form.cleaned_data['preview']
                post.body = post_form.cleaned_data['body']
                post.pub_date = timezone.now()

                post.save(update_fields=['pub_date', 'preview', 'body'])

                # Record slug for redirect
                slug = post.slug

            # Redirect user to gallery
            return redirect('/blog/view/' + slug)
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
        'home_text': helpers.randomize_home_text(),
        'nbar': 'Blog',
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
        'home_text': helpers.randomize_home_text(),
        'nbar': 'Blog',
        'title': post.title,
        'slug': slug,
        'pub_date': post.pub_date,
        'body': markdown(post.body),
    }

    return render(request, 'blog/view.html', context=context)


def post_gallery(request):
    '''
    View previews of all posts (separated into pages)
    '''
    # Order posts from most recent to oldest
    posts = models.BlogPostModel.objects.all().order_by('-id')

    context = {
        'home_text': helpers.randomize_home_text(),
        'nbar': 'Blog',
        'posts': posts,
    }

    return render(request, 'blog/gallery.html', context=context)


def resume(request, file_name='resume.pdf', my_name='Jake_Hansen'):
    '''
    Display resume as PDF
    '''
    path = join(settings.MEDIA_ROOT, file_name)

    return HttpResponse(open(path, 'rb').read(), content_type='application/pdf')
