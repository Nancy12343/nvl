__author__ = 'tq'
from django.conf.urls import url, patterns
from .views import *

urlpatterns = patterns('',
    url(r'^home/$', IndexView.as_view(), name='home'),
    url(r'^detail/$', DetailView.as_view(), name='detail'),
    url(r'^thechapter/(?P<pk>\d+)/$', ChapterView.as_view(), name='chapter'),
    url(r'^thecomment/$', CommentsView.as_view(), name='comment'),
    url(r'^subtype/$', show_subtype, name='subtype'),
    url(r'^writerInfo/(?P<pk>\d+)/$', WriterInfo.as_view(), name='writerInfo'),
    url(r'^addNovel/$', AddNovelView.as_view(), name='addNovel'),
    url(r'^edit/$', EditView.as_view(), name='edit'),
    url(r'^downloadChapter/$', file_download, name='download_chapter'),
    url(r'^search/$', SearchView.as_view(), name='search'),

)
