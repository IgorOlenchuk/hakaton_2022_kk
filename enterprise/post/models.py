from django.db import models


class PostPage(models.Model):
    title = models.CharField(max_length=80,
                             help_text='Длина до 80 символов (в идеале на менее 40 и не более 70), заполнять обязательно',
                             verbose_name='SEO Title')
    description = models.CharField(max_length=200,
                                   blank=True,
                                   help_text='длина до 200 символов (в идеале до 160)',
                                   verbose_name='SEO Description')
    h1 = models.CharField(max_length=100,
                          help_text='Заголовок h1 до 100 символов',
                          verbose_name='Заголовок')
    mini_description = models.CharField(max_length=100,
                                        blank=True,
                                        help_text='Описание страницы под заголовком до 100 символов',
                                        verbose_name='Описание страницы')
    text = models.TextField(blank=True,
                            help_text='Основной текст страницы, количество символов не ограничено',
                            verbose_name='Основной текст страницы')
    image = models.ImageField(upload_to='post/',
                              verbose_name='Изображение поста',
                              blank=True,
                              null=True)

    class Meta:
        verbose_name = 'Пост',
        verbose_name_plural = 'Пост'

    def __str__(self):
        return self.h1
