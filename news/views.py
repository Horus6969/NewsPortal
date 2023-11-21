from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostForm, UserForm
from .models import Post, Category
from .filters import PostFilter
from .tasks import notify_new_post


class Posts(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


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


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == reverse('news_create'):
            post.type_post = 'NW'
        else:
            post.type_post = 'AR'
        post.save()
        notify_new_post.delay(post.pk)
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'


class AuthorUpdate(LoginRequiredMixin, UpdateView):
    form_class = UserForm
    model = User
    template_name = 'author.html'
    context_object_name = 'author'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')


class CategoryList(ListView):
    model = Post
    ordering = '-time_create'
    context_object_name = 'categories'
    template_name = 'category_list.html'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['is_subscriber'] = self.request.user in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    email = user.email
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    html = render_to_string(
        'mail/subscribed.html',
        {
            'category': category,
            'user': user,
        }
    )

    msg = EmailMultiAlternatives(
        subject=f"Подписка на категорию {category}",
        body='',
        from_email='DEFAULT_FROM_EMAIL',
        to=[email, ]
    )
    msg.attach_alternative(html, 'text/html')

    msg.send()

    return redirect('posts')


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    return redirect('posts')
