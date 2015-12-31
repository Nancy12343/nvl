from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Comment(models.Model):

    chapter = models.ForeignKey('Chapter', related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments')
    content = models.CharField(max_length=512, blank=True, null=True)
    comment_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):

        return '%s_%s_%s' %(self.chapter, self.user, self.comment_time)


class Chapter(models.Model):
    VIP_TRUE = 1
    VIP_FALSE = 0
    VIP_CHOICES = (
        (VIP_FALSE, _('not VIP')),
        (VIP_TRUE, _('VIP'))
    )
    LAST_CHAPTER_TRUE = 1
    LAST_CHAPTER_FALSE = 0
    LAST_CHAPTER_CHOICE = (
        (LAST_CHAPTER_FALSE, _('not last chapter')),
        (LAST_CHAPTER_TRUE, _('last chapter'))
    )
    FIRST_CHAPTER_TRUE = 1
    FIRST_CHAPTER_FALSE = 0
    FIRST_CHAPTER_CHOICE = (
        (FIRST_CHAPTER_FALSE, _('not first chapter')),
        (FIRST_CHAPTER_TRUE, _('first chapter'))
    )

    novelDetail = models.ForeignKey('NovelDetail', related_name='chapter')
    title = models.CharField(max_length=512, blank=True, null=True)
    is_vip = models.IntegerField(choices=VIP_CHOICES, default=VIP_FALSE)
    publish_time = models.DateTimeField(auto_now=True)
    is_last_chapter = models.IntegerField(choices=LAST_CHAPTER_CHOICE, default=LAST_CHAPTER_FALSE)
    is_first_chapter = models.IntegerField(choices=FIRST_CHAPTER_CHOICE, default=FIRST_CHAPTER_FALSE)
    content = models.FileField(upload_to='static/files', blank=True, null=True)
    pre_chapter = models.OneToOneField('self', related_name='next_chapter', blank=True, null=True)

    def __unicode__(self):
        return '%s_%s' %(self.novelDetail.name, self.title)


class NovelSection(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return '%s' %self.name.strip()

class NovelDetail(models.Model):
    FINISH_TRUE = 1
    FINISH_FALSE = 0
    FINISH_CHOICE = (
        (FINISH_TRUE, _('Finished')),
        (FINISH_FALSE, _('Not Finish'))
    )

    name = models.CharField(max_length=512)
    novelSection = models.ManyToManyField(NovelSection, through='SectionDetail', related_name='novel_detail')
    point = models.IntegerField(default=0)
    # author register in the site
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    # author not register in the site
    author = models.CharField(max_length=255, blank=True, null=True)
    is_finish = models.IntegerField(choices=FINISH_CHOICE, default=FINISH_FALSE)
    sumary = models.TextField(blank=True, null=True)
    last_edit = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='static/image')
    click_count = models.BigIntegerField(default=0)

    def __unicode__(self):
        return '%s' %self.name.strip()


class SectionDetail(models.Model):
    novelDetail = models.ForeignKey(NovelDetail, related_name='section_detail')
    novelSection = models.ForeignKey(NovelSection, related_name='section_detail')

    def __unicode__(self):
        return '%s_%s' %(self.novelSection, self.novelDetail)

    class Meta:
        db_table = 'novels_novelsection_noveldetail'




