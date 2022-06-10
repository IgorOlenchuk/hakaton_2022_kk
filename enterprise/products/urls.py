from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('group/<int:group_id>', views.group_products, name='group'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('favorites', views.FavoriteView.as_view(), name='favorite'),
    path('favorites/<int:product_id>', views.delete_favorite,
         name='delete_favorite'),
    path('products/new', views.new_product, name='new_product'),
    path('products/<int:product_id>', views.product_detail,
         name='product'),
    path('products/<int:product_id>/edit', views.edit_product,
         name='edit_product'),
    path('products/<int:product_id>/delete', views.delete_product,
         name='delete_product'),
    path('purchases', views.PurchaseView.as_view(), name='purchases'),
    path('purchases/<int:product_id>', views.delete_purchase,
         name='delete_purchase'),
    #path('shoplist', views.send_shop_list, name='shop-list'),
]
