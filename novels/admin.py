__author__ = 'tq'
from django.contrib import admin
from .models import NovelSection, NovelDetail, SectionDetail, Chapter, Comment

admin.site.register(NovelSection)
admin.site.register(NovelDetail)
admin.site.register(SectionDetail)
admin.site.register(Chapter)
admin.site.register(Comment)