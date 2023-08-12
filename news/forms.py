from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Post, Author


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=50)

    class Meta:
        model = Post
        fields = [
            'category',
            'header',
            'text',
            'author'
        ]
        labels = {
            'category': 'Категория',
            'header': 'Заголовок',
            'text': 'Текст',
            'author': 'Автор'
        }

    def clean(self):
        cleaned_data = super().clean()
        header = cleaned_data.get("header")
        text = cleaned_data.get("text")

        if header == text:
            raise ValidationError(
                "Заголовок не должнен быть идентичен тексту публикаци."
            )

        return cleaned_data

class UserForm(forms.ModelForm):
    class Meta:
        model = User

        fields = ['username',
                  'password',
                  'email'
                  ]
