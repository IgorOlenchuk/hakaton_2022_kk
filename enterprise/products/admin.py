from django.contrib import admin
from .models import Products, Groups, Favorite


class ProductsAdmin(admin.ModelAdmin):

    list_display = ('pk', 'name', 'description', 'pub_date', 'price', 'group', 'in_favorite_count')
    search_fields = ('groups', 'name',)
    list_filter = ('group', 'price', 'pub_date',)
    empty_value_display = '-пусто-'

    def in_favorite_count(self, obj):
        return obj.favorite_set.count()

    in_favorite_count.short_description = 'В избранном'


class GroupsAdmin(admin.ModelAdmin):

    list_display = ('pk', 'title')
    search_fields = ('title',)
    list_filter = ('title',)
    empty_value_display = '-пусто-'


class FavoriteAdmin(admin.ModelAdmin):
    model = Favorite
    list_display = ('pk', 'user', 'show_products',)

    def show_products(self, obj):
        products = obj.products.all()
        return '\n'.join([product.name for product in products])


admin.site.register(Products, ProductsAdmin)
admin.site.register(Groups, GroupsAdmin)
admin.site.register(Favorite, FavoriteAdmin)
