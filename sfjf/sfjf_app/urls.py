from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from markdownx import urls as markdownx

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('resume', views.resume, name='resume'),
    path('blog', views.post_gallery, name='post gallery'),
    path('blog/edit', views.edit_post, name='new post'),
    path('blog/edit/<slug:slug>', views.edit_post, name='edit post'),
    path('blog/view/<slug:slug>', views.view_post, name='view post'),
    url(r'^markdownx/', include(markdownx)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
