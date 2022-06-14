# Generated by Django 3.1.6 on 2022-06-14 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PostPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='Длина до 210 символов, заполнять не обязательно', max_length=210, verbose_name='SEO Title')),
                ('description', models.CharField(blank=True, help_text='длина до 450 символов', max_length=450, verbose_name='SEO Description')),
                ('h1', models.CharField(help_text='Заголовок h1 до 100 символов', max_length=100, verbose_name='Заголовок')),
                ('mini_description', models.CharField(blank=True, help_text='Описание страницы под заголовком до 100 символов', max_length=100, verbose_name='Описание страницы')),
            ],
            options={
                'verbose_name': ('Пост',),
                'verbose_name_plural': 'Пост',
            },
        ),
    ]
