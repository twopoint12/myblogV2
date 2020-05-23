import markdown
import re
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, TemplateView
from markdown.extensions.toc import TocExtension
from pure_pagination.mixins import PaginationMixin
from .models import Article, Category, Like, Tag


class IndexView(PaginationMixin, ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'
    paginate_by = 10


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = 'article'

    def get(self, request, *args, **kwargs):
        response = super(ArticleDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response


class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchiveView, self).get_queryset().filter(created_time__year=year,
                                                              created_time__month=month)


class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class TagView(IndexView):
    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=t)


def search(request):
    q = request.GET.get('q')

    if not q:
        error_msg = '请输入搜索关键词'
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('blog:index')

    article_list = Article.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'article_list': article_list})


class AboutSiteView(TemplateView):
    template_name = 'blog/about_site.html'


class AboutMeView(TemplateView):
    template_name = 'blog/about_me.html'


def update_likes(request):
    if request.method == 'POST':
        article_id = request.POST['articleId']
        article = Article.objects.get(id=article_id)
        ip = get_ip(request)
        insert_success = Like.objects.get_or_create(ip=ip, article=article)[1]
        if insert_success:
            json_response = JsonResponse({"status": "insert success"}, safe=False)
        else:
            json_response = JsonResponse({"status": "insert fail"}, safe=False)
        return json_response


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
    return ip

