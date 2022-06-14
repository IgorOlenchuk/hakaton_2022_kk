from django.contrib import admin
from .models import Products, Groups


class ProductsAdmin(admin.ModelAdmin):

    list_display = ('pk', 'name', 'description', 'pub_date', 'price', 'group')
    search_fields = ('groups', 'name',)
    list_filter = ('group', 'price', 'pub_date',)
    empty_value_display = '-пусто-'


class GroupsAdmin(admin.ModelAdmin):

    list_display = ('pk', 'title')
    search_fields = ('title',)
    list_filter = ('title',)
    empty_value_display = '-пусто-'


admin.site.register(Products, ProductsAdmin)
admin.site.register(Groups, GroupsAdmin)
