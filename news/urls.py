from django.urls import path
from .views import NewsList, NewsDetail, ArticleList, ArticleDetail

urlpatterns = [
    path('news/', NewsList.as_view()),
    path('news/<int:pk>', NewsDetail.as_view()),
    path('article/', ArticleList.as_view()),
    path('article/<int:pk>', ArticleDetail.as_view())
]
