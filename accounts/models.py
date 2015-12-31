# coding=utf-8
from django.db import models
from django.conf import settings

class Account(models.Model):
    READER = 0
    WRITER = 1
    READER_TO_WRITER = 2
    ROLE_CHOICE = (
        (READER, '读者'),
        (WRITER, '作者'),
        (READER_TO_WRITER, '申请作者')
    )
    name = models.CharField(max_length=255)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, default=None, related_name='account')
    role = models.IntegerField(choices=ROLE_CHOICE, default=READER)
    last_edit = models.DateField(auto_now=True)
    point = models.IntegerField(default=10)
    email = models.EmailField()

    def __unicode__(self):
        return '%s' %self.name.strip()


