from django.urls import path
from django.conf.urls import url, include
from markdownx import urls as markdownx

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/edit', views.edit_post, name='new post'),
    path('blog/edit/<slug:slug>', views.edit_post, name='edit post'),
    #path('blog/<slug:slug>', views.view_post, name='view post'),
    url(r'^markdownx/', include(markdownx)),
]
