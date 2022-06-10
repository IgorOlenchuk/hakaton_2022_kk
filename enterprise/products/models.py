from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist


User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название группы товаров')
    image = models.ImageField(upload_to='products/group/',
                              verbose_name='Изображение группы товаров')
    slug = models.SlugField(unique=True, verbose_name='Слаг группы')

    def __str__(self):
        return f'{self.title}'


class ProductManager(models.Manager):
    def group_filter(self, groups):
        if groups:
            return super().get_queryset().prefetch_related(
                'groups'
            ).filter(
                groups__slug__in=groups
            ).distinct()
        else:
            return super().get_queryset().prefetch_related(
                'groups'
            ).all()


class Products(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название товара')
    description = models.TextField(verbose_name='Описание товара')
    image = models.ImageField(upload_to='products/',
                              verbose_name='Изображение твоара')
    groups = models.ForeignKey(Group,
                              on_delete=models.SET_NULL,
                              related_name='group_products',
                              blank=True, null=True)
    price = models.IntegerField(verbose_name='Цена')
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Время добавления', db_index=True)

    products = ProductManager()

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.name}'


class PurchaseManager(models.Manager):
    def counter(self, user):
        try:
            return super().get_queryset().get(user=user).products.count()
        except ObjectDoesNotExist:
            return 0

    def get_purchases_list(self, user):
        try:
            return super().get_queryset().get(user=user).products.all()
        except ObjectDoesNotExist:
            return []

    def get_user_purchase(self, user):
        try:
            return super().get_queryset().get(user=user)
        except ObjectDoesNotExist:
            purchase = Purchase(user=user)
            purchase.save()
            return purchase


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Products)

    purchase = PurchaseManager()


class FavoriteManager(models.Manager):
    def get_favorites(self, user):
        try:
            return super().get_queryset().get(user=user).products.all()
        except ObjectDoesNotExist:
            return []

    def get_group_filtered(self, user, tags):
        try:
            products = super().get_queryset().get(user=user).products.all()
            if groups:
                return products.prefetch_related(
                    'groups'
                ).filter(
                    groups__slug__in=groups
                ).distinct()
            else:
                return products.prefetch_related(
                    'groups'
                ).all()
        except ObjectDoesNotExist:
            return []

    def get_user(self, user):
        try:
            return super().get_queryset().get(user=user)
        except ObjectDoesNotExist:
            favorite_user = Favorite(user=user)
            favorite_user.save()
            return favorite_user


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Products)

    favorite = FavoriteManager()

