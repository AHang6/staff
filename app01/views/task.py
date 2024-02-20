import json
from django import forms
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app01.models import Task
from app01.utils.bootstrap import BootstrapModelForm
from app01.utils.pagination import Pagination


class TaskModelForm(BootstrapModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'detail': forms.TextInput
        }


def task_list(request):
    """   任务列表   """
    form = TaskModelForm()
    queryset = Task.objects.all().order_by('-id')
    page_obj = Pagination(request, queryset, page_size=5)

    context = {
        'form': form,
        'queryset': page_obj.page_queryset,
        'page_string': page_obj.html(),
    }

    return render(request, 'task_list.html', context)


@csrf_exempt
def task_ajax(request):
    # print(request.GET)
    print(request.POST)
    data_dict = {'status': True, 'data': [11, 22, 33, 44]}
    return HttpResponse(json.dumps(data_dict))


@csrf_exempt
def task_add(request):
    print(request.POST)

    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {'status': True}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))
