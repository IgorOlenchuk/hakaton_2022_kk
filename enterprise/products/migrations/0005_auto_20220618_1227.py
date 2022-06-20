# Generated by Django 3.1.6 on 2022-06-18 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20220616_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='alt_image_description_first',
            field=models.TextField(blank=True, help_text='Длина до 160 символов (в идеале на менее 40 и не более 160), заполнять обязательно', max_length=160, null=True, verbose_name='Описание изображения для SEO'),
        ),
        migrations.AlterField(
            model_name='products',
            name='alt_image_description_second',
            field=models.TextField(blank=True, help_text='Длина до 160 символов (в идеале на менее 40 и не более 160), заполнять обязательно', max_length=160, null=True, verbose_name='Описание изображения для SEO'),
        ),
    ]
