from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 0、排除那些不需要登录就能访问的页面
        #       request.path_info    获取当前用户请求的url
        if request.path_info in ['/account/login/', '/image/code/']:
            return

        # 1、读取当前访问的用户的session信息，如何能读到，说明已登录过，就可以继续向后执行
        info_dict = request.session.get('info')
        if info_dict:
            return

        # 2、没登录过得重新返回登录界面
        return redirect('/account/login/')
