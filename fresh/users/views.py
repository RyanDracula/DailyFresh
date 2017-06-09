# coding:utf-8
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import JsonResponse, HttpResponseRedirect
from .models import UserInfo, AdrressInfo, MyCart
from goods.models import *
from django.core.paginator import Paginator
from .user_decorater import login_or_not
from django.shortcuts import render_to_response
from django.template import RequestContext


def register(request):
    """注册页面"""
    return render(request, 'users/register.html')


def verify_name(request):
    """验证用户名是否已经被注册"""
    user_name = request.GET.get('user_name')
    num = UserInfo.objects.filter(uname=user_name).count()
    return JsonResponse({'num': num})


def verify_email(request):
    """验证用户邮箱是否已经被注册"""
    email = request.GET.get('email')
    num = UserInfo.objects.filter(email=email).count()
    return JsonResponse({'num': num})


def handle_register(request):
    """用户注册，将用户信息存入数据库"""
    po = request.POST
    user_name = po.get('user_name')
    pwd = po.get('pwd')
    email = po.get('email')
    UserInfo.objects.create(uname=user_name, upwd=pwd, email=email)
    return redirect('/user/login.html')


def go_login(request):
    """登录时的验证模块"""
    print request.method
    # 判断是否是POST请求，如果不是（非提交操作），直接重定向到login.html
    if request.method != 'POST':
        return redirect('/user/login.html')
    else:
        go = request.POST
        # 获取用户名，密码，是否勾选“记住用户名”的信息
        user_name = go.get('username')
        pwd = go.get('pwd')
        checked = go.get('check', '')
        try:
            user = UserInfo.objects.get(uname=user_name)
        except ObjectDoesNotExist, MultipleObjectsReturned:
            return render_to_response('users/login.html', {'error': 1, 'u_name': user_name, 'u_pwd': pwd}, context_instance=RequestContext(request))
        else:
            if user.upwd == pwd:
                # 登录成功，跳转到登录前的页面
                url = request.COOKIES.get('url', '')
                if url:
                    response = HttpResponseRedirect(url)
                else:
                    response = HttpResponseRedirect('/goods/index.html')
                # 清除以前的cookie（其他用户登录时的最近浏览信息）
                response.set_cookie('recentlysee', '', max_age=-1)
                # 如果用户选择记住用户名
                if checked:
                    # 将用户名写入浏览器cookie，下次登录时记住用户名
                    response.set_cookie('user_name', user_name)
                else:
                    # 否则让用户名立即过期
                    response.set_cookie('user_name', '', max_age=-1)
                # 将用户名和id写入session
                request.session['user_name'] = user_name
                request.session['user_id'] = user.id
                # request.session.set_expiry(3600)
                return response
            else:
                # 使用render_to_response传递参数时，避免csrf错误，需加context_instance属性
                return render_to_response('users/login.html', {'error': 1, 'u_name': user_name, 'u_pwd': pwd}, context_instance=RequestContext(request))


def login(request):
    """登录页面，登录时获取cookies中用户名信息（验证是否勾选“记住用户名”）"""
    cooki = request.COOKIES.get('user_name', '')
    # 需要检测用户名是否在数据库中吗？
    return render(request, 'users/login.html', {'cooki': cooki})


@login_or_not
def add_minus(request):
    # 通过$.get构造的参数，需通过request.GET.get接收
    goods_id = int(request.GET.get('goodsID'))
    count = int(request.GET.get('count'))
    per_id = int(request.session['user_id'])
    # 先读取此用户购物车中的这个商品
    goods = MyCart.objects.filter(per_id_id=per_id).filter(goods_id_id=goods_id)
    count = int(count)
    goods.update(count=count)
    return JsonResponse({'success': 'yes', 'count': count})


@login_or_not
def add_cart(request, gid, count):
    goods_id = int(gid)
    count = int(count)
    per_id = int(request.session['user_id'])
    # 先读取此用户购物车中的这个商品
    good_list = MyCart.objects.filter(per_id_id=per_id).filter(goods_id_id=goods_id)
    # 如果存在此商品（即filter返回了查询集），就让此商品数量增加；
    if good_list:
        count += good_list[0].count
        good_list.update(count=count)
    # 如果不存在此商品，即返回空列表，此时创建此商品
    else:
        MyCart.objects.create(count=count, per_id_id=per_id, goods_id_id=goods_id)
    # 判断是否是ajax异步请求，如果是返回Json数据（detail页面的ajax请求,或者购物车页面的ajax）
    if request.is_ajax():
        return JsonResponse({'goods_count': MyCart.objects.filter(per_id_id=per_id).count()})

    return redirect('/user/cart.html')


@login_or_not
def cart(request):
    user_name = request.session.get('user_name', "")
    per_id = int(request.session['user_id'])
    my_goods = MyCart.objects.filter(per_id_id=per_id)
    # isCart用于在模板继承时识别购物车页面，还是用户中心页面
    context = {'isCart': 'yes', 'my_goods': my_goods, 'user_name': user_name}
    return render(request, 'users/content/cart.html', context)


@login_or_not
def user_center_site(request):
    user_name = request.session.get('user_name', "")
    user_id = int(request.session['user_id'])
    addrinfo = AdrressInfo.objects.filter(user_id=user_id)
    if addrinfo:
        addrinfo = addrinfo[0]
    context = {'addrinfo': addrinfo, 'info': 'site', 'user_name': user_name}
    return render(request, 'users/content/user_center_site.html', context)


@login_or_not
def get_site(request):
    """存入用户的收获地址"""
    go = request.POST
    recv_people = go.get('recv_people', '')
    recv_address = go.get('recv_address')
    youbian = go.get('youbian', '')
    telephone = go.get('telephone')
    uid = request.session.get('user_id', "")
    if uid:
        # 如果收货地址存在，更新此地址
        myAddr = AdrressInfo.objects.filter(user_id=uid)
        if myAddr:
            myAddr.update(person=recv_people, addr=recv_address, youbian=youbian, tel=telephone, user_id=uid)
        else:
            AdrressInfo.objects.create(person=recv_people, addr=recv_address, youbian=youbian, tel=telephone, user_id=uid)
    return redirect('/user/user_center_site.html')


@login_or_not
def user_center_order(request, page_id):
    if not page_id:
        page_id = 1
    user_name = request.session.get('user_name', "")
    print user_name
    user = UserInfo.objects.get(uname=user_name)
    # 数据表关系为多对一，“－”的一方，可直接使用_set查询
    orders = user.orderinfo_set.all()
    p = Paginator(orders, 2)
    # 得到某一页的数据
    page_id = int(page_id)
    pages = p.page(page_id)
    # 总页数
    count_pages = p.num_pages
    # 得到所有的页码信息（列表）
    plist = p.page_range
    minus = count_pages - page_id
    if count_pages > 5:
        if page_id in (1, 2):
            plist = plist[0:5]
        elif page_id in (count_pages-1, count_pages-2, count_pages):
            plist = plist[page_id-(5-minus):page_id+minus]
        else:
            plist = plist[page_id-3:page_id+2]
    context = {'info': 'order', 'user_name': user_name, 'pages': pages, 'count_pages': count_pages,
               'page_id': page_id, 'plist': plist}
    return render(request, 'users/content/user_center_order.html', context)


@login_or_not
def user_center_info(request):
    # 在session中查询到user_id，构造此用户对象
    user_name = request.session.get('user_name', "")
    user_id = int(request.session['user_id'])
    goodslist = []
    userobj = UserInfo.objects.get(id=user_id)
    # 如果用户已经添加过地址，获取地址信息
    addrobj = AdrressInfo.objects.filter(user_id=user_id)
    if addrobj:
        addrobj = addrobj[0]
    # 从cookies中拿出用户的最近浏览字段
    recentlysaw = request.COOKIES.get('recentlysee', '')
    if recentlysaw:
        # 商品ID存在，遍历ID，构建对应的商品对象
        recentlysaw = recentlysaw.split(',')
        for i in recentlysaw:
            try:
                goods = GoodsInfo.objects.get(id=int(i))
            except ObjectDoesNotExist:
                pass
            else:
                goodslist.append(goods)
    context = {'userobj': userobj, 'addrobj': addrobj, 'goodslist': goodslist, 'info': 'info', 'user_name': user_name}
    return render(request, 'users/content/user_center_info.html', context)


# 退出
def logout(request):
    response = HttpResponseRedirect('/user/index.html')
    # 清理session里保存username
    del request.session['user_name']
    del request.session['user_id']
    # 使用redirect会直接跳转到此链接
    return redirect('/goods/index.html')

# 入坑：
# 1. views 的第一个参数必须是request，其余参数由urls中的正则(分组)传递
# 2. render 和 redirect(HttpResponseRedirect) 有什么区别？

# 3. 本可以直接使用redirect，错误的使用了render_to_response，造成add_cart页面刷新会报错，如下错误代码：
# my_goods = MyCart.objects.filter(per_id_id=per_id)
# context = {'isCart': 'yes', 'my_goods': my_goods}
# return render_to_response('users/content/cart.html', context, context_instance=RequestContext(request))
# 为什么会犯这个错误？（没有理解重定向）
# 使用redirect，浏览器会直接访问url链接，此时又要经历urls->views->templates的查找
# 而使用render_to_response，只会将当前view指向template，不进行urls->views的查找过程

# 4. 对数据库中已有信息进行更新时，save,update有什么区别？

# 5. $.get('/user/add_minus'+show_goodsID+'/00', function (data) {})直接构造的地址，接收参数时需要在url处正则匹配，传递的参数是正则分组
# 和$.get('/user/add_minus', {'goodsID': goodsID, 'count': count}, function (data){})构造的地址，传递的参数，
# 需要在views里request.GET.get('goodsID')接收
