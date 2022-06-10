from django.contrib import admin
from .models import Products, Group, Favorite


class ProductsAdmin(admin.ModelAdmin):

    list_display = ('pk', 'name', 'description', 'pub_date', 'price', 'groups', 'in_favorite_count')
    search_fields = ('groups', 'name',)
    list_filter = ('groups', 'price', 'pub_date',)
    empty_value_display = '-пусто-'

    def in_favorite_count(self, obj):
        return obj.favorite_set.count()

    in_favorite_count.short_description = 'В избранном'


class GroupAdmin(admin.ModelAdmin):

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
admin.site.register(Group, GroupAdmin)
admin.site.register(Favorite, FavoriteAdmin)
