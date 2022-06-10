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
from .models import Favorite, Group, Products, Purchase, User


def _extend_context(context, user):
    context['purchase_list'] = Purchase.purchase.get_purchases_list(user)
    context['favorites'] = Favorite.favorite.get_favorites(user)
    return context


@require_GET
def index(request):
    groups = request.GET.getlist('group')
    product_list = Products.products.group_filter(groups)
    paginator = Paginator(product_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'all_groups': Group.objects.all(),
        'group': groups,
        'page': page,
        'paginator': paginator
    }
    user = request.user
    if user.is_authenticated:
        context['active'] = 'product'
        _extend_context(context, user)
    return render(request, 'index.html', context)


def group_products(request, slug):
    group = get_object_or_404(Group, slug=slug)
    products = group.group_products.all()
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context ={
        'page': page,
        'paginator': paginator,
        'group': group,
        'products': products,
    }
    return render(request, 'group.html', context)

@require_GET
def profile(request, user_id):
    profile = get_object_or_404(User, id=user_id)
    groups = request.GET.getlist('group')
    products_list = Products.products.group_filter(groups)
    paginator = Paginator(products_list.filter(author=profile), 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'all_groups': Group.objects.all(),
        'profile': profile,
        'page': page,
        'paginator': paginator
    }
    # Если юзер авторизован, добавляет в контекст список избранное
    user = request.user
    if user.is_authenticated:
        _extend_context(context, user)
    return render(request, 'profile.html', context)


@require_GET
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    context = {
        'group': group,
    }
    user = request.user
    if user.is_authenticated:
        _extend_context(context, user)
    return render(request, 'group_detail.html', context)


@require_GET
def product_detail(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    context = {
        'product': product,
    }
    user = request.user
    if user.is_authenticated:
        _extend_context(context, user)
    return render(request, 'product_detail.html', context)


class FavoriteView(View):
    model = Favorite

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        groups = self.request.GET.getlist('group')
        user = self.request.user
        queryset = self.model.favorite.get_group_filtered(user, groups)
        return queryset

    def get(self, request):
        paginator = Paginator(self.get_queryset(), 6)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        purchase_list = Purchase.purchase.get_purchases_list(request.user)
        context = {
            'all_groups': Group.objects.all(),
            'purchase_list': purchase_list,
            'active': 'favorite',
            'paginator': paginator,
            'page': page
        }
        return render(request, 'favorites.html', context)

    def post(self, request):
        json_data = json.loads(request.body.decode())
        recipe_id = json_data['id']
        recipe = get_object_or_404(Products, id=product_id)
        data = {'success': 'true'}
        favorite = Favorite.favorite.get_user(request.user)
        is_favorite = favorite.products.filter(id=product_id).exists()
        if is_favorite:
            data['success'] = 'false'
        else:
            favorite.recipes.add(product)
        return JsonResponse(data)


@login_required(login_url='auth/login/')
@require_http_methods('DELETE')
def delete_favorite(request,product_id):
    product = get_object_or_404(Products, id=product_id)
    data = {'success': 'true'}
    try:
        favorite = Favorite.favorite.get(user=request.user)
    except ObjectDoesNotExist:
        data['success'] = 'false'
    if not favorite.products.filter(id=product_id).exists():
        data['success'] = 'false'
    favorite.products.remove(product)
    return JsonResponse(data)


class PurchaseView(View):
    model = Purchase

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = self.model.purchase.get_purchases_list(self.request.user)
        return queryset

    def get(self, request):
        products_list = self.get_queryset()
        context = {
            'products_list': products_list,
            'active': 'purchase'
        }
        return render(request, 'purchases.html', context)

    def post(self, request):
        json_data = json.loads(request.body.decode())
        product_id = json_data['id']
        product = get_object_or_404(Products, id=product_id)
        purchase = Purchase.purchase.get_user_purchase(user=request.user)
        data = {
            'success': 'true'
        }
        if not purchase.recipes.filter(id=product_id).exists():
            purchase.products.add(product)
            return JsonResponse(data)
        data['success'] = 'false'
        return JsonResponse(data)


@login_required(login_url='auth/login/')
@require_http_methods('DELETE')
def delete_purchase(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    data = {
        'success': 'true'
    }
    try:
        purchase = Purchase.purchase.get(user=request.user)
    except ObjectDoesNotExist:
        data['success'] = 'false'
    if not purchase.products.filter(id=product_id).exists():
        data['success'] = 'false'
    purchase.products.remove(product)
    return JsonResponse(data)


@login_required
@require_http_methods(['GET', 'POST'])
def new_product(request):
    context = {
        'active': 'new_product',
        'page_title': 'Создание товара',
        'button_label': 'Создать товар',
    }
    # GET-запрос на страницу создания рецепта
    if request.method == 'GET':
        form = ProductForm()
        context['form'] = form
        return render(request, 'product_form.html', context)
    # POST-запрос с данными из формы создания рецепта
    elif request.method == 'POST':
        form = ProductForm(request.POST, files=request.FILES or None)
        if not form.is_valid():
            context['form'] = form
            return render(request, 'product_form.html', context)
        product = form.save(commit=False)
        product.author = request.user
        form.save()
        return redirect('index')


@login_required
@require_http_methods(['GET', 'POST'])
def edit_product(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    context = {
        'product': product,
        'product_id': product_id,
        'page_title': 'Редактирование товара',
        'button_label': 'Сохранить',
    }
    # GET-запрос на страницу редактирования товара
    if request.method == 'GET':
        form = ProductForm(instance=product)
        context['form'] = form
        return render(request, 'product_form.html', context)
    # POST-запрос с данными из формы редактирования товара
    elif request.method == 'POST':
        form = ProductForm(request.POST or None,
                          files=request.FILES or None, instance=product)
        if not form.is_valid():
            context['form'] = form
            return render(request, 'product_form.html', context)
        form.save()
        return redirect('index')


@login_required(login_url='auth/login/')
@require_GET
def delete_product(request, product_id):
    recipe = get_object_or_404(Products, id=product_id)
    recipe.delete()
    return redirect('index')


def page_not_found(request, exception):
    context = {'path': request.path}
    return render(request, 'misc/404.html', context, status=404)
