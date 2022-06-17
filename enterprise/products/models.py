from django.db import models
from django.contrib.auth import get_user_model


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
    seo_title = models.TextField(max_length=70,
                                   help_text='Длина до 70 символов (в идеале на менее 40 и не более 70), заполнять обязательно',
                                   verbose_name='seo_title товара')
    seo_description = models.TextField(max_length=160,
                                   help_text='Длина до 160 символов (в идеале на менее 40 и не более 160), заполнять обязательно',
                                   verbose_name='seo_description товара')
    mini_description = models.TextField(max_length=160,
                                   help_text='Длина до 160 символов (в идеале на менее 40 и не более 160), заполнять обязательно',
                                   verbose_name='Краткое описание товара')
    image = models.ImageField(upload_to='group/products/',
                              help_text='Изображение товара для главной страницы',
                              verbose_name='Изображение товара 1',
                              blank=True,
                              null=True)
    alt_image = models.TextField(max_length=160,
                                 help_text='Длина до 160 символов (в идеале на менее 40 и не более 160), заполнять обязательно',
                                 verbose_name='Описание изображения для SEO')
    description = models.TextField(max_length=160,
                                   help_text='Длина до 160 символов (в идеале на менее 40 и не более 160), заполнять обязательно',
                                   verbose_name='Основное описание товара')
    description_first = models.TextField(help_text='Полное описание товара - часть 1',
                                         verbose_name='Полное описание товара - часть 1',
                                         blank=True,
                                         null=True)
    description_second = models.TextField(help_text='Полное описание товара - часть 2',
                                          verbose_name='Полное описание товара - часть 2',
                                          blank=True,
                                          null=True)
    image_description_first = models.ImageField(upload_to='group/products/',
                                                help_text='Изображение товара для части описания 1',
                                                verbose_name='Изображение товара 2',
                                                blank=True,
                                                null=True)
    alt_image_description_first = models.TextField(max_length=160,
                                                   help_text='Длина до 160 символов (в идеале на менее 40 и не более 160), заполнять обязательно',
                                                   verbose_name='Описание изображения для SEO',
                                                   blank=True,
                                                   null=True)
    image_description_second = models.ImageField(upload_to='group/products/',
                                                 help_text='Изображение товара для части описания 2',
                                                 verbose_name='Изображение товара 3',
                                                 blank=True,
                                                 null=True)
    alt_image_description_second = models.TextField(max_length=160,
                                                    help_text='Длина до 160 символов (в идеале на менее 40 и не более 160), заполнять обязательно',
                                                    verbose_name='Описание изображения для SEO',
                                                    blank=True,
                                                    null=True)
    characteristic = models.TextField(help_text='Характеристики',
                                      verbose_name='Характеристики',
                                      blank=True,
                                      null=True)
    image_characteristic = models.ImageField(upload_to='group/products/',
                                                 help_text='Изображение товара для Характеристики',
                                                 verbose_name='Изображение товара 3',
                                                 blank=True,
                                                 null=True)
    alt_image_characteristic = models.TextField(max_length=160,
                                                help_text='Длина до 160 символов (в идеале на менее 40 и не более 160), заполнять обязательно',
                                                verbose_name='Описание изображения для SEO',
                                                blank=True,
                                                null=True)
    group = models.ForeignKey(Groups,
                              on_delete=models.SET_NULL,
                              related_name='group_products',
                              verbose_name='Группа товара',
                              blank=True, null=True)
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Время добавления', db_index=True)

    products = ProductManager()

    class Meta:
        verbose_name = 'Товары',
        verbose_name_plural = 'Товары'
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.name}'
