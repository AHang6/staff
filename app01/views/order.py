import json
import random
from decimal import Decimal
from datetime import datetime
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app01.models import Order
from app01.utils.bootstrap import BootstrapModelForm
from app01.utils.pagination import Pagination


class OrderAddModelForm(BootstrapModelForm):
    class Meta:
        model = Order
        # fields = '__all__'
        exclude = ['oid', 'user']


def order_list(request):
    form = OrderAddModelForm()
    queryset = Order.objects.all().order_by('-id')
    page_obj = Pagination(request, queryset)

    context = {
        'form': form,
        'queryset': page_obj.page_queryset,
        'page_string': page_obj.html(),
    }
    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    """"    新建订单（Ajax)请求        """
    form = OrderAddModelForm(data=request.POST)

    if form.is_valid():
        # 添加订单号(自己后台生成）
        form.instance.oid = datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(1000, 9999))

        # 固定值设置管理员ID
        form.instance.user_id = request.session['info']['id']
        form.save()
        data_dict = {'status': True}
        return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

    data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))


def order_delete(request):
    nid = request.GET.get('nid')
    exists = Order.objects.filter(id=nid).exists()
    if exists:
        Order.objects.filter(id=nid).delete()
        data_dict = {'status': True}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {'status': False, 'error': '数据错误，信息删除失败'}
    return HttpResponse(json.dumps(data_dict))


# 是decimal数据  json序列化

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def order_edit(request):
    nid = request.GET.get('nid')
    row_dict = Order.objects.filter(id=nid).values('title', 'price', 'status').first()
    if not row_dict:
        data_dict = {'statis': False, 'error': "信息错误，数据传输失败"}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {'status': True, 'data': row_dict}
    return HttpResponse(json.dumps(data_dict, cls=DecimalEncoder))


@csrf_exempt
def order_editSave(request):
    nid = request.GET.get('nid')
    row_obj = Order.objects.filter(id=nid).first()
    if not row_obj:
        data_dict = {'static': False, 'tips': '信息错误，请刷新页面'}
        return HttpResponse(json.dumps(data_dict))

    form = OrderAddModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        data_dict = {'status': True}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict))


