from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from app01.models import Admin
from app01.utils.pagination import Pagination
from app01.utils.form import AdminModelForm, AdminEditModelForm, AdminResetModelForm


def admin_list(request):
    """   管理员列表    """

    # 构造搜索条件
    data_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        data_dict['username__contains'] = search_data

    # 根据搜索条件搜索数据库数据
    queryset = Admin.objects.filter(**data_dict)
    page_obj = Pagination(request, queryset)
    context = {
        'search_data': search_data,

        'queryset': page_obj.page_queryset,
        'page_string': page_obj.html()
    }

    return render(request, 'admin_list.html', context)


def admin_add(request):
    """  添加管理员   """
    title = '新建管理员'
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, 'change.html', {'form': form, 'title': title})

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    return render(request, 'change.html', {'form': form})


def admin_edit(request, nid):
    """   编辑管理员   """
    title = '编辑管理员'
    row_obj = Admin.objects.filter(id=nid).first()
    if request.method == "GET":

        if not row_obj:
            return redirect('/admin/list/')

        form = AdminEditModelForm(instance=row_obj)

        return render(request, 'change.html', {'form': form, 'title': title})

    form = AdminEditModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    return render(request, 'change.html', {'form': form, 'title': title})


def admin_delete(request, nid):
    """   删除用户   """
    # Admin.objects.filter(id=nid).delete()
    Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')


def admin_reset(request, nid):
    row_obj = Admin.objects.filter(id=nid).first()
    title = '重置密码 - {}'.format(row_obj.username)

    if request.method == 'GET':
        form = AdminResetModelForm()
        return render(request, 'change.html', {'form': form, 'title': title})

    form = AdminResetModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    return render(request, 'change.html', {'form': form, 'title': title})


