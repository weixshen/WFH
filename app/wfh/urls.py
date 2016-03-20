from django.conf.urls import url

from . import views

app_name = 'wfh'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<article_id>[0-9]+)/$', views.words, name='words'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^known/$', views.known, name='known'),
    url(r'^readed/$', views.readed, name='readed'),
]
