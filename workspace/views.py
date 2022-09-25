from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from .workspace_services import *


@login_required(login_url='/staff/login/')
def workspace(request):
    data_objects, table_head, header = get_table_data_for_user(request.user)
    paginator = Paginator(data_objects.order_by('id'), 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'data': page_obj,
        'table_head': table_head,
        'header': header
    }
    return render(request, 'workspace/workspace.html', context)

