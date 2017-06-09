# coding:utf-8
import functools
from django.http import HttpResponseRedirect, JsonResponse


# 如果未登录则转到登录页面
def login_or_not(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        uname = request.session.get('user_name', '')
        uid = request.session.get('user_id', '')
        if uname and uid:
            return func(request, *args, **kwargs)
        else:
            # 需判断是否是ajax的操作（添加购物车的请求），如果是ajax请求，需返回Json数据
            if request.is_ajax():
                return JsonResponse({'no_login': 'yes'})
            else:
                return HttpResponseRedirect('/user/login.html')
                # red = HttpResponseRedirect('/user/login.html')
                # red.set_cookie('url', request.get_full_path())
                # return red
    return wrapper