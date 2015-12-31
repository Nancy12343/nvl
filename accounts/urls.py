__author__ = 'tq'
from django.conf.urls import patterns, url

from .views import LoginView, RegistView, LogoutView

urlpatterns = patterns('',
    url(r'^$', LoginView.as_view(), name='login'),
    url(r'^regist/$', RegistView.as_view(), name='regist'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

)

