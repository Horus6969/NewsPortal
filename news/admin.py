from django.contrib import admin
from .models import Post

class ProductAdmin(admin.ModelAdmin):
    list_display = ('header', 'author', 'rating', 'type_post', 'time_create', 'get_category')
    list_filter = ('rating', 'type_post',)
    search_fields = ('header', 'author__user__username', 'type_post')

admin.site.register(Post,ProductAdmin)
