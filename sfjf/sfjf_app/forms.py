from django import forms
from markdownx.fields import MarkdownxFormField

class BlogPostForm(forms.Form):
    '''
    Create or edit blog post
    '''
    title = forms.CharField(max_length=256)
    image = forms.ImageField(required=False)
    body = MarkdownxFormField()
