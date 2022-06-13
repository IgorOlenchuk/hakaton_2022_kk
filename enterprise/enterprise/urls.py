from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path


handler404 = 'products.views.page_not_found'  # noqa

urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/', include('users.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('', include('products.urls')),
]

urlpatterns += [
    path('about/', include("django.contrib.flatpages.urls")),
    path("about/about-author/", views.flatpage,
         {"url": "/about-author/"}, name="about-author"),
    path("about/about-spec/", views.flatpage,
         {"url": "/about-spec/"}, name="about-spec"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATICFILES_DIRS)
