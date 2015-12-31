__author__ = 'tq'
# -*- coding:utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

class ChapterForm(forms.Form):
    LAST_CHAPTER_TRUE = 1
    LAST_CHAPTER_FALSE = 0
    LAST_CHAPTER_CHPICE = (
        (LAST_CHAPTER_FALSE, _('False')),
        (LAST_CHAPTER_TRUE, _('True'))
    )

    title = forms.CharField(max_length=255, required=True, label='Title')
    is_last = forms.ChoiceField(choices=LAST_CHAPTER_CHPICE, label='Is Last Chapter', widget=forms.Select)
    content = forms.FileField(label='content')




