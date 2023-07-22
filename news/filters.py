from django import forms
from django_filters import FilterSet, ModelChoiceFilter, CharFilter, DateFilter
from .models import Author


class PostFilter(FilterSet):
    header = CharFilter(field_name='header',
                        lookup_expr='icontains',
                        label='Заголовок'
                        )
    author = ModelChoiceFilter(field_name='author',
                               queryset=Author.objects.all(),
                               label='Автор'
                               )
    time_create = DateFilter(field_name='time_create', lookup_expr='gt',
                             label='Дата публикации не позже',
                             widget=forms.DateInput(attrs={'type': 'date'}))
