"""annomathtex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
# Django imports
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views.annotate_formula_view import FileUploadView
from .views.render_file_view import RenderFileView
from .views.test_view import test_view

urlpatterns = [
    # Examples:
    # url(r'^blog/', include('blog.urls', namespace='blog')),

    # provide the most basic login/logout functionality
    #url(r'^login/$', auth_views.login,
    #    {'template_name': 'core/login.html'}, name='core_login'),
    #url(r'^logout/$', auth_views.logout, name='core_logout'),

    # enable the admin interface
    url(r'^admin/', admin.site.urls),
    url(r'', FileUploadView.as_view()),
    #url(r'^file_upload/', FileUploadView.as_view()),
    url(r'^render_file/', RenderFileView.as_view()),
    url(r'^test/', test_view)

]
