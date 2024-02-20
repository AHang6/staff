from django.shortcuts import render, redirect
from app01.models import Mobile_Num
from app01.utils.pagination import Pagination
from app01.utils.form import MobileModelForm, MobileEditModelForm


# Create your views here.


def mobile_list(request):
    data_dict = {}
    search_data = request.GET.get('q', '')

    # 拼接url的链接
    # import copy
    #
    # query_dict = copy.deepcopy(request.GET)
    # query_dict._mutable = True
    # query_dict.setlist('page', [11])
    # query_dict.urlencode()

    # 搜索功能
    if search_data:
        data_dict['mobile__contains'] = search_data

    queryset = Mobile_Num.objects.filter(**data_dict).all().order_by('-level')

    pagination = Pagination(request, queryset)

    context = {
        'search_data': search_data,

        'queryset': pagination.page_queryset,
        'page_string': pagination.html()
    }

    return render(request, 'mobile_list.html', context)


def mobile_add(request):
    if request.method == 'GET':
        form = MobileModelForm()
        return render(request, 'mobile_add.html', {'form': form})

    form = MobileModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/mobile/list/')

    return render(request, 'mobile_add.html', {'form': form})


def mobile_edit(request, nid):
    row_obj = Mobile_Num.objects.filter(id=nid).first()
    if request.method == "GET":
        form = MobileEditModelForm(instance=row_obj)
        return render(request, 'mobile_edit.html', {'form': form})

    form = MobileEditModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/mobile/list/')
    return render(request, 'mobile_edit.html', {'form': form})


def mobile_delete(request, nid):
    Mobile_Num.objects.filter(id=nid).delete()
    return redirect('/mobile/list/')


