from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('group/<int:group_id>', views.group_products, name='group'),
    path('products/<int:product_id>', views.product_detail,
         name='product'),
]
