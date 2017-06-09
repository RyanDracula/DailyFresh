# coding:utf-8
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.template import loader,RequestContext
from .models import TypeInfo, GoodsInfo
from django.core.paginator import Paginator
from users.models import UserInfo, MyCart

# Create your views here.


def get_uname(request):
    """发起ajax请求，验证用户是否已登录"""
    uname = request.session.get('user_name', "")
    return JsonResponse({'login_user_name': uname})


def index(request):
    """首页"""
    user_name = request.session.get('user_name', "")
    all_list = []
    goods_info = {}
    for i in range(1, 7):
        # 获取分类名称
        goods_info['type_obj'] = TypeInfo.objects.get(id=i).title
        # 商品类型的id
        goods_info['type_id'] = i
        # 按照id逆序排序（最新商品）
        goods_info['default_order'] = GoodsInfo.objects.filter(gtype_id=i).order_by('-id')[0:4]
        # 按点击量排序
        goods_info['click_goods'] = GoodsInfo.objects.filter(gtype_id=i).order_by('-gclick')[0:3]
        all_list.append(goods_info)
        goods_info = {}
    # has_cart用于模板继承时，区分首页/(详情页,商品列表页)
    context = {'all_list': all_list, 'has_cart': "1", 'user_name': user_name, 'cart_count': cart_count(request)}
    return render(request, 'goods/index.html', context)


def detail(request, gid):
    user_name = request.session.get('user_name', "")
    # 构造商品对象(id在数据库中是int类型)
    goodslist = GoodsInfo.objects.filter(id=int(gid))
    # 如果商品存在才返回结果
    if goodslist:
        n = goodslist[0].gclick + 1
        # 使用update更新点击数（按人气排序）
        goodslist.update(gclick=n)
        # 商品分类对象
        typeobj = TypeInfo.objects.get(id=goodslist[0].gtype_id)
        # 最新发布的两条商品信息
        newest = GoodsInfo.objects.filter(gtype_id=int(typeobj.id)).order_by('-id')[0:2]
        # 构造返回的数据
        response = render(request, 'goods/detail.html', {'goodsInfo': goodslist[0], 'typeobj': typeobj,
                                                         'newest': newest, 'user_name': user_name, 'cart_count': cart_count(request)})
        previous = request.COOKIES.get('recentlysee', '')
        # 如果此cookie已经存在，就修改此内容
        if previous:
            previous = previous.split(',')
            # 如果此元素已经出现过，就将原来的记录删除
            if gid in previous:
                previous.remove(gid)
            # 将此商品编号放到最新
            previous.insert(0, gid)
            # 元素数大于５时，删除最后的元素
            if len(previous) > 5:
                previous.pop()
            previous = ','.join(previous)
            response.set_cookie('recentlysee', previous)
        # 如果不存在创建此条cookie
        else:
            response.set_cookie('recentlysee', '{0}'.format(gid))
        return response


def lists(request, tid, page_id, order_id):
    user_name = request.session.get('user_name', "")
    # 获取分类名称
    type_obj = TypeInfo.objects.get(id=int(tid)).title
    # 按照id倒序排序，得到“最新”发布的商品对象
    newest = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')[0:2]
    # 定制　url->排序方式　的映射
    dic = {'order1': '-id', 'order2': 'gprice', 'order3': '-gclick'}
    orderby = order_id.encode('utf-8')
    if not order_id:
        orderby = 'order1'
    # 按照规则进行排序，得到所有结果
    list1 = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by(dic[orderby])
    # 对所有结果进行分页
    p = Paginator(list1, 15)
    # 得到某一页的数据
    page1 = p.page(int(page_id))
    # 总页码
    count_pages = p.num_pages
    # 得到所有的页码信息（列表）
    plist = p.page_range
    # page1传递本页商品/分页信息，tid传递此分类id，page_id传递此页数，count_pages传递总页数，plist传递页数(列表)，
    # ordeby传递根据此条件排序，newest传递最新的两条商品信息
    return render(request, 'goods/list.html',
                  {'page1': page1, 'tid': int(tid), 'page_id': page_id, 'count_pages': count_pages,'cart_count': cart_count(request),
                   'plist': plist, 'orderby': orderby, 'newest': newest, 'type_obj': type_obj, 'user_name': user_name})


from haystack.views import SearchView


class MySearchView(SearchView):
    def extra_context(self):
        extra = super(MySearchView, self).extra_context()
        extra['title']=self.request.GET.get('q')
        extra['cart_count']=cart_count(self.request)
        return extra


# 传递回购物车中商品数量
def cart_count(request):
    if 'user_id' in request.session:
        return MyCart.objects.filter(per_id_id=request.session['user_id']).count()
    else:
        return 0

