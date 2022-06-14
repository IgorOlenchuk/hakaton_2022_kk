from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist


User = get_user_model()


class Groups(models.Model):
    title = models.CharField(max_length=70,
                             verbose_name='Название группы товаров',
                             help_text='Длина до 70 символов (в идеале на менее 40 и не более 70), заполнять обязательно')
    image = models.ImageField(upload_to='group/',
                              help_text='желательно 480х480, качество для web',
                              verbose_name='Изображение группы товаров')

    class Meta:
        verbose_name = 'Группы товаров',
        verbose_name_plural = 'Группы товаров'

    def __str__(self):
        return f'{self.title}'


class ProductManager(models.Manager):
    def group_filter(self, group):
        if group:
            return super().get_queryset().prefetch_related(
                'groups'
            ).filter(
                groups__slug__in=group
            ).distinct()
        else:
            return super().get_queryset().prefetch_related(
                'groups'
            ).all()


class Products(models.Model):
    name = models.CharField(max_length=70,
                            help_text='Длина до 70 символов (в идеале на менее 40 и не более 70), заполнять обязательно',
                            verbose_name='Название товара')
    description = models.TextField(max_length=300,
                                   help_text='Длина до 300 символов (в идеале на менее 40 и не более 160), заполнять обязательно',
                                   verbose_name='Описание товара')
    image = models.ImageField(upload_to='group/products/',
                              verbose_name='Изображение товара',
                              blank=True,
                              null=True)
    group = models.ForeignKey(Groups,
                              on_delete=models.SET_NULL,
                              related_name='group_products',
                              verbose_name='Группа товара',
                              blank=True, null=True)
    price = models.IntegerField(verbose_name='Цена',
                                blank=True,
                                null=True)
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Время добавления', db_index=True)

    products = ProductManager()

    class Meta:
        verbose_name = 'Товары',
        verbose_name_plural = 'Товары'
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.name}'
