from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET
from .models import Products
from post import models as post


@require_GET
def index(request):
    seodata = post.PostPage.objects.all()
    product_list = Products.products.all()
    paginator = Paginator(product_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'seodata': seodata,
        'paginator': paginator
    }
    user = request.user
    if user.is_authenticated:
        context['active'] = 'product'
    return render(request, 'index.html', context)


@require_GET
def product_detail(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    context = {
        'product': product,
    }
    return render(request, 'product_detail.html', context)


def page_not_found(request, exception):
    context = {'path': request.path}
    return render(request, 'misc/404.html', context, status=404)
