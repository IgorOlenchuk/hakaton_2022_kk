from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET
from .models import Products
import pandas as pd
import numpy as np
from .methods import do_work, file_time


@require_GET
def index(request):
    context = {
        'file_time': do_work()
    }
    return render(request, 'index.html', context)


def page_not_found(request, exception):
    context = {'path': request.path}
    return render(request, 'misc/404.html', context, status=404)
