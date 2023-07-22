from datetime import datetime

from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostForm
from .models import Post
from .filters import PostFilter


class Posts(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostSearch(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'posts_search.html'
    context_object_name = 'search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filterset'] = self.filterset
        return context


class NewsList(ListView):
    queryset = Post.objects.filter(type_post='NW')
    ordering = '-time_create'
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10


class NewsDetail(DetailView):
    queryset = Post.objects.filter(type_post='NW')
    template_name = 'news.html'
    context_object_name = 'news'


class ArticlesList(ListView):
    queryset = Post.objects.filter(type_post='AR')
    ordering = '-time_create'
    template_name = 'articles_list.html'
    context_object_name = 'articles_list'
    paginate_by = 10

class ArticlesDetail(DetailView):
    queryset = Post.objects.filter(type_post='AR')
    template_name = 'article.html'
    context_object_name = 'article'


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == reverse('news_create'):
            post.type_post = 'NW'
        else:
            post.type_post = 'AR'
        return super().form_valid(form)


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')
