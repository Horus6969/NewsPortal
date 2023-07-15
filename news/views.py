from datetime import datetime
from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    queryset = Post.objects.filter(type_post='NW')
    ordering = '-time_create'
    template_name = 'news_list.html'
    context_object_name = 'news_list'


class NewsDetail(DetailView):
    queryset = Post.objects.filter(type_post='NW')
    template_name = 'news.html'
    context_object_name = 'news'


class ArticleList(ListView):
    queryset = Post.objects.filter(type_post='AR')
    ordering = '-time_create'
    template_name = 'article_list.html'
    context_object_name = 'article_list'


class ArticleDetail(DetailView):
    queryset = Post.objects.filter(type_post='AR')
    template_name = 'article.html'
    context_object_name = 'article'
