import json
from urllib.parse import unquote

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import (require_GET, require_http_methods,
                                          require_POST)
from users.models import Subscription

from .forms import ProductForm
from .models import Groups, Products, User
from post import models as post


@require_GET
def index(request):
    seodata = post.PostPage.objects.all()
    product_list = Products.products.all()
    paginator = Paginator(product_list, 8)
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


def group_products(request, group_id):
    group = get_object_or_404(Groups, id=group_id)
    products_list = group.group_products.all()
    paginator = Paginator(products_list, 12)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context ={
        'page': page,
        'paginator': paginator,
        'group': group,
        'all_products': products_list,
    }
    return render(request, 'group.html', context)


@require_GET
def group_detail(request, group_id):
    group = get_object_or_404(Groups, id=group_id)
    context = {
        'group': group,
    }
    return render(request, 'group_detail.html', context)


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
