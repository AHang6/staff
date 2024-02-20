from django.http import JsonResponse
from django.shortcuts import render, HttpResponse


def chart_list(request):
    return render(request, 'chart_list.html')


def chart_bar(request):
    legend_list = ['张三', '赵云']
    x_axis = ['1月', '2月', '3月', '4月', '5月', '6月']
    series = [
        {
            "name": '张三',
            "type": 'bar',
            "data": [5, 20, 36, 10, 10, 20]
        },
        {
            "name": '赵云',
            "type": 'bar',
            "data": [15, 30, 15, 40, 30, 50]
        }
    ]

    result = {
        'status': True,
        'data': {
            'legend_list': legend_list,
            'x_axis': x_axis,
            'series': series,
        }

    }

    return JsonResponse(result)


def chart_pie(request):
    data_list = [
        {"value": 1048, "name": 'IT部分'},
        {"value": 735, "name": '运营部门'},
        {"value": 580, "name": '新媒体'},
    ]

    result = {
        'status': True,
        'data_list': data_list,
    }
    return JsonResponse(result)


def chart_line(request):
    legend_list = ['上海', '广西']
    x_axis = ['1月', '2月', '3月', '4月', '5月', '6月', '7月']
    series = [
        {
            "name": '上海',
            "type": 'line',
            "data": [5, 20, 36, 10, 10, 20, 20]
        },
        {
            "name": '广西',
            "type": 'line',
            "data": [15, 30, 15, 40, 30, 50, 60]
        }
    ]

    result = {
        'status': True,
        'data': {
            'legend_list': legend_list,
            'x_axis': x_axis,
            'series': series
        }
    }

    return JsonResponse(result)
