from django.contrib import admin
from .models import PostPage


class PostPageAdmin(admin.ModelAdmin):
    list_display = ('h1',)


admin.site.register(PostPage, PostPageAdmin)
