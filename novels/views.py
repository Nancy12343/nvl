# coding:utf-8
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import FormView
from .models import NovelDetail, NovelSection, Chapter, Comment, SectionDetail
from django.shortcuts import redirect, render, render_to_response
from django.core.urlresolvers import reverse, reverse_lazy
from braces.views import LoginRequiredMixin
import datetime
from accounts.models import Account
from django.contrib.auth.models import User
from .forms import ChapterForm
from django.http import StreamingHttpResponse, Http404
from django.template import RequestContext
from braces.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

def handle_404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

@login_required
def file_download(request):

    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    the_file_name = request.GET.get('file')
    if not the_file_name:
        raise Http404
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response

class IndexView(TemplateView):
    template_name = 'novels/home.html'

    def get(self, request, *args, **kwargs):

        return super(IndexView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super(IndexView,self).get_context_data(**kwargs)
        totalTop = NovelDetail.objects.order_by('-click_count')
        sections = NovelSection.objects.all()
        sections_list = []
        for section in sections:
            details = section.section_detail.all()
            sections_data = {}
            sections_data['details'] = details[:4]
            sections_data['name'] = section.name
            sections_data['id'] = section.id
            sections_list.append(sections_data)
        latest = NovelDetail.objects.order_by('-last_edit')
        context_data['sections'] = sections_list
        context_data['totalTop'] = totalTop[:10]
        # only show four latest books
        context_data['latest'] = latest[:4]
        return context_data

class DetailView(TemplateView):
    template_name = 'novels/detail.html'

    def get(self, request, *args, **kwargs):

        return super(DetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super(DetailView, self).get_context_data(**kwargs)
        novel_id = self.request.GET.get('pk')
        detail = NovelDetail.objects.get(pk=novel_id)
        if detail:
            try:
                detail.click_count += 1
                detail.save()
            except:
                pass
            chapters = Chapter.objects.filter(novelDetail=detail)
            context_data['novelDetail'] = detail
            context_data['chapters'] = chapters
            sections = detail.novelSection.all()
            section = ''
            for s in sections:
                section = section + s.name + '     '
            context_data['section'] = section
        else:
            raise Http404
        return context_data

class ChapterView(TemplateView):
    template_name = 'novels/chapter.html'

    def get(self, request, *args, **kwargs):
        return super(ChapterView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super(ChapterView, self).get_context_data(**kwargs)
        pk = kwargs['pk']
        chapter = Chapter.objects.get(pk=pk)
        if chapter:
            # increase the click count of the novel
            try:
                novelDetail = chapter.novelDetail
                novelDetail.click_count += 1
                novelDetail.save()
            except:
                pass
            next_chapter = Chapter.objects.filter(pre_chapter=chapter)
            if next_chapter:
                context_data['next_chapter'] = next_chapter[0]
            novelDetail = chapter.novelDetail
            context_data['chapter'] = chapter
            context_data['novelDetail'] = novelDetail
            comments = Comment.objects.filter(chapter=chapter)
            context_data['comments'] = comments
        else:
            raise Http404
        return context_data

class CommentsView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        content = self.request.GET.get('content')
        chapterId = self.request.GET.get('chapterId', 4)
        user = self.request.user
        comment = Comment()
        chapter = Chapter.objects.filter(pk=chapterId)
        if chapter:
            comment.chapter = chapter[0]
            comment.user = user
            comment.content = content
            comment.comment_time = datetime.datetime.now()
            comment.save()
        return redirect(reverse('novels:chapter', args=(chapterId,)))

def show_subtype(request):
    section_id = request.GET.get('section')
    section = NovelSection.objects.filter(pk=section_id)
    template_name = 'novels/subtype.html'
    if section:
        novelDetails = NovelDetail.objects.filter(novelSection=section)

    return render(request, template_name, {'novelDetails':novelDetails})

class WriterInfo(TemplateView):
    template_name = 'novels/writer_info.html'

    def get(self, request, *args, **kwargs):
        return super(WriterInfo, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        writer_user = User.objects.filter(pk=pk)
        if writer_user:
            writer_user = writer_user[0]
            account = Account.objects.filter(user=writer_user)
        if account:
            account = account[0]
            account.role = 1
            account.save()
        return super(WriterInfo, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super(WriterInfo, self).get_context_data(**kwargs)
        pk = kwargs['pk']
        writer_user = User.objects.filter(pk=pk)
        if writer_user:
            writer_user = writer_user[0]
            account = Account.objects.filter(user=writer_user)
        if account:
            account = account[0]
            context_data['account'] = account
            role = account.role
            if role == Account.READER:
                context_data['role'] = "reader"
            elif role == Account.WRITER:
                context_data['role'] = "writer"
            else:
                context_data['role'] = "to be writer"
            novelDetails = NovelDetail.objects.filter(writer=writer_user)
            novelSections = NovelSection.objects.all().distinct()
            context_data['novelSections'] = novelSections
            detail_data = []
            for novelDetail in novelDetails:
                novel_sections = novelDetail.novelSection.all()
                sections = ""
                for s in novel_sections:
                    sections = sections + s.name + '    '
                data = {
                    'image': novelDetail.image,
                    'name': novelDetail.name,
                    'novelSection': sections,
                    'is_finish': novelDetail.is_finish,
                    'id': novelDetail.id
                }
                detail_data.append(data)

            context_data['novelDetails'] = detail_data

        return context_data

class AddNovelView(View):

    def post(self, request, *args, **kwargs):
        section = self.request.POST.get('section')
        novelName = self.request.POST.get('novelName')
        sumary = self.request.POST.get('sumary')
        image = self.request.FILES['imageAddr']
        user = request.user
        try:
            novelsection = NovelSection.objects.filter(name=section)
            if novelsection:
                novelsection = novelsection[0]
            # add to novel detail
            noveldetail = NovelDetail()
            noveldetail.name = novelName
            noveldetail.sumary = sumary
            noveldetail.image = image
            noveldetail.writer = user
            noveldetail.last_edit = datetime.datetime.now()
            noveldetail.save()
            # add to section detail
            sectiondetail = SectionDetail()
            sectiondetail.novelSection = novelsection
            sectiondetail.novelDetail = noveldetail
            sectiondetail.save()
        except:
            pass

        return redirect(reverse('novels:writerInfo', args=(self.request.user.id,)))

class EditView(FormView):
    template_name = "novels/edit.html"
    form_class = ChapterForm

    def get(self, request, *args, **kwargs):
        return super(EditView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(EditView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        title = form.cleaned_data.get("title")
        is_last = form.cleaned_data.get("is_last")
        content = form.cleaned_data.get("content")
        self.novel_id = self.request.GET.get('id')
        chapter = Chapter()
        novelDetail = NovelDetail.objects.filter(pk=self.novel_id)
        if novelDetail:
            novelDetail = novelDetail[0]
            chapter.novelDetail = novelDetail
            chapter.is_last_chapter = is_last
            # import ipdb;ipdb.set_trace()
            # utf8_file = codecs.open(content, "rb", encoding="utf-8")
            chapter.content = content
            chapter.title = title
            if novelDetail.chapter.all():
                chapter.is_first_chapter = False
                pre_chapter = novelDetail.chapter.all().order_by('-publish_time')[0]
                chapter.pre_chapter = pre_chapter
            else:
                chapter.is_first_chapter = True
            chapter.save()
            return super(EditView, self).form_valid(form)

    def get_success_url(self):
        return "%s?id=%s" % (reverse("novels:edit"), self.novel_id)

    def get_context_data(self, **kwargs):
        context_data = super(EditView, self).get_context_data(**kwargs)
        self.novel_id = self.request.GET.get('id')
        novelDetail = NovelDetail.objects.filter(pk=self.novel_id)
        if novelDetail:
            novelDetail = novelDetail[0]
            context_data['novelDetail'] = novelDetail
            chapters = Chapter.objects.filter(novelDetail=novelDetail)
            context_data['chapters'] = chapters
        return context_data

class SearchView(TemplateView):
    template_name = 'novels/search.html'

    def get(self, request, *args, **kwargs):
        return super(SearchView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        searchCondition = request.POST.get('searchCondition').encode('UTF-8')
        searchContext = request.POST.get('searchContext')
        data = {}
        novelDetail = []
        if searchCondition == '作者':
            novelDetail = NovelDetail.objects.filter(writer__username__contains=searchContext)
        elif searchCondition == '书名':
            novelDetail = NovelDetail.objects.filter(name__contains=searchContext)
        data['novelDetails'] = novelDetail
        return render(request, self.template_name, data)
