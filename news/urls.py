from django.urls import path
from .views import NewsList, NewsDetail, ArticlesList, ArticlesDetail, Posts, PostSearch, PostCreate, PostUpdate, \
    PostDelete

urlpatterns = [
    path('',Posts.as_view(), name='posts'),
    path('news/', NewsList.as_view(), name='news'),
    path('news/<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('articles/', ArticlesList.as_view(), name='articles'),
    path('articles/<int:pk>', ArticlesDetail.as_view(), name='article_detail'),
    path('search/', PostSearch.as_view(), name='search'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('article/create/', PostCreate.as_view(), name='article_create'),
    path('news/<int:pk>/update', PostUpdate.as_view(), name='news_update'),
    path('article/<int:pk>/update', PostUpdate.as_view(), name='article_update'),
    path('news/<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
    path('article/<int:pk>/delete', PostDelete.as_view(), name='article_delete'),
]
