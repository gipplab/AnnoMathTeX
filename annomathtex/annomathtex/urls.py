"""annomathtex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
# Django imports
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views.annotation_view import AnnotationView
from .views.start_screen_view import StartScreenView
from .views.test_view import TestView

from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .settings import common


urlpatterns = [
    # Examples:
    # url(r'^blog/', include('blog.urls', namespace='blog')),

    # provide the most basic login/logout functionality
    #url(r'^login/$', auth_views.login,
    #    {'template_name': 'core/login.html'}, name='core_login'),
    #url(r'^logout/$', auth_views.logout, name='core_logout'),

    # enable the admin interface
    url(r'^admin/', admin.site.urls),
    url(r'^annotation/', AnnotationView.as_view()),
    url(r'^test/', TestView.as_view()),
    url(r'', StartScreenView.as_view())
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(common.MEDIA_URL, document_root=common.MEDIA_ROOT)

