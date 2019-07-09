from django.shortcuts import render

def home(request):
    '''
    Render homepage
    '''
    return render(request, 'base.html')

def edit_post(request, slug=''):
    '''
    Create or edit a blog post
    '''

    if slug != '':
        # Fetch the information for the post we are trying to edit
        post_queryset = models.BlogPostModel.objects.filter(slug=slug)

        post = post_queryset[0] if len(post_queryset) else None
        if post is None:
            raise ValueError('No post identified by slug "{}"'.format(slug))

        # TODO: load data from post and fit into form

    if request.method == 'POST':
        post_form = forms.BlogPostForm(request.POST, request.FILES)
        if post_form.is_valid():
            # Get slug so we can identify the post
            slug = slugify(post_form.cleaned_data['title'])
        else:
            raise ValueError('Submitted form is invalid')
