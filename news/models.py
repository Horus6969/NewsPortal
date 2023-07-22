from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        author_rating_post = Post.objects.filter(author_id=self.pk).aggregate(r1=Coalesce(Sum('rating'), 0))['r1']
        author_rating_comment = Comment.objects.filter(user_id=self.user).aggregate(r2=Coalesce(Sum('rating'), 0))['r2']
        author_rating_post_comment = \
        Comment.objects.filter(post__author__user=self.user).aggregate(r3=Coalesce(Sum('rating'), 0))['r3']

        self.rating = author_rating_post * 3 + author_rating_comment + author_rating_post_comment
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=70, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    article = 'AR'
    news = 'NW'
    post_type = [
        (article, 'Статья'),
        (news, 'Новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    type_post = models.CharField(max_length=2, choices=post_type)
    time_create = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=150)
    text = models.TextField(default='Пост')
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.header.title()} : {self.text}, {self.time_create}"

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...' if len(self.text) > 124 else self.text

    def get_absolute_url(self):
        return reverse('posts')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.CharField(max_length=2000)
    time_create = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
