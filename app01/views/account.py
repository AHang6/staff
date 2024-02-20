from django.shortcuts import render, redirect, HttpResponse
from io import BytesIO

from app01.utils.form import LoginForm
from app01.utils.image_code import check_code
from app01.models import Admin


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)

    if form.is_valid():
        image_input_code = form.cleaned_data.pop('image_code')
        code = request.session.get('image_code', '')
        admin_obj = Admin.objects.filter(**form.cleaned_data).first()
        if image_input_code.upper() != code.upper():
            form.add_error('image_code', '验证码错误')
            return render(request, 'login.html', {'form': form})

        if not admin_obj:
            form.add_error('password', '用户名或密码错误请重新输入')
            return render(request, 'login.html', {'form': form})

        request.session['info'] = {'id': admin_obj.id, 'username': admin_obj.username, 'password': admin_obj.password}
        # 设置session时间为7天
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect('/admin/list/')

    return render(request, 'login.html', {'form': form})


def logout(request):
    request.session.clear()
    return redirect('/login/')


def image_code(request):
    img, code_string = check_code()
    print(code_string)

    # 写入自己的session中，（以便于后续获取验证码校验）
    request.session['image_code'] = code_string
    # 给Session设置60s超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def image_reset(request):
    img, code_string = check_code()
    print(code_string)

    # 写入自己的session中，（以便于后续获取验证码校验）
    request.session['image_code'] = code_string
    # 给Session设置60s超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
