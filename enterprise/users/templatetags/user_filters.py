from django import template


register = template.Library()


@register.filter
def url_with_get(request, page):
    query = request.GET.copy()
    query['page'] = page
    return query.urlencode()


@register.filter
def add_color(group):
    colors = {
        'breakfast': 'orange',
        'lunch': 'green',
        'dinner': 'purple'
    }
    return colors[group.slug]


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def subtract(number_1, number_2):
    return int(number_1) - int(number_2)


@register.filter
def get_groups(request):
    return request.getlist('group')


@register.filter
def renew_group_link(request, group):
    request_copy = request.GET.copy()
    groups = request_copy.getlist('group')
    if group.slug in groups:
        groups.remove(group.slug)
        request_copy.setlist('group', groups)
    else:
        request_copy.appendlist('group', group.slug)
    return request_copy.urlencode()
