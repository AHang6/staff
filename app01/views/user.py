from django.shortcuts import render, redirect
from app01.utils.pagination import Pagination
from app01.utils.form import UserModelForm
from app01.models import UserInfo, Department


# Create your views here.
def user_list(request):
    """  用户列表  """
    queryset = UserInfo.objects.all()

    # for i in range(1, 100):
    #     UserInfo.objects.create(name='张三', password='123456', age=19, account=10.2, create_time='2021-11-11', depart_id=1, gender=1)

    page_obj = Pagination(request, queryset)

    for obj in queryset:
        print(obj.id, obj.name, obj.password, obj.age, obj.account, obj.create_time.strftime("%Y-%m-%d"),
              obj.depart.title, obj.get_gender_display()),

    context = {
        'queryset': page_obj.page_queryset,
        'page_string': page_obj.html(),
    }

    return render(request, "user_list.html", context)


def user_add(request):
    """  添加用户（原始方法）  """

    if request.method == "GET":
        context = {
            'gender_choices': UserInfo.gender_choices,
            'depart_list': Department.objects.all(),
        }

        return render(request, "user_add.html", context)

    # 获取用户提交的数据

    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    account = request.POST.get('account')
    ctime = request.POST.get('ctime')
    depart_id = request.POST.get('depart_id')
    gender = request.POST.get('gender')

    UserInfo.objects.create(name=user, password=pwd, age=age,
                            account=account, create_time=ctime,
                            depart_id=depart_id, gender=gender)

    return redirect("/user/list/")


def user_delete(request, nid):
    """  删除用户   """
    UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list')


def user_edit(request, nid):
    """  编辑用户  """
    context = {
        'user_info': UserInfo.objects.filter(id=nid).all().first(),
        'depart_list': Department.objects.all(),
        'gender_choices': UserInfo.gender_choices,
    }
    return render(request, 'user_edit.html', context)


def user_model_from_add(request):
    """   添加用户  （ModelFrom版本）   """
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_model_from_add.html', {'form': form})

    # 用户用POST提交数据，数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        # {'name': '赵晨航', 'password': '123456', 'age': 29, 'account': Decimal('4000'), 'create_time': datetime.date(2021, 11, 11), 'gender': 1, 'depart': <Department: IT运维部>}
        # print(form.cleaned_data)
        form.save()
        return redirect('/user/list/')

    # 校验失败（在页面上显示错误信息）
    # print(form.errors)
    return render(request, 'user_model_from_add.html', {'form': form})


def user_model_edit(request, nid):
    """  编辑用户   """

    row_object = UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        # 将数据库对象，通过instance 传入modelForm对象中即可
        form = UserModelForm(instance=row_object)
        return render(request, 'user_model_edit.html', {'form': form})

    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # form.instance.字段名 = '值'
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_model_edit.html', {'form': form})
