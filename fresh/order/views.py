# _*_coding: utf-8_*_
from django.shortcuts import render, redirect
from goods.models import GoodsInfo
from .models import OrderInfo, OrderDetail
from users.models import MyCart, AdrressInfo, UserInfo
from django.db import transaction
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
import datetime

# Create your views here.


def place_order(request):
    user_name = request.session.get('user_name', "")
    cartsID = request.GET.getlist('cart_id')
    if cartsID:
        goods = MyCart.objects.filter(id__in=cartsID)
        # 如果地址不存在，转去填写地址
        try:
            addr = AdrressInfo.objects.get(user_id=goods[0].per_id_id)
        except ObjectDoesNotExist:
            return redirect('/user/user_center_site.html')
        context = {'isCart': 'order', 'goods': goods, 'addr': addr, 'user_name': user_name}
        return render(request, 'order/place_order.html', context)


@transaction.atomic
def submit_order(request):
    """使用事务，完成生成订单"""
    post = request.POST
    address = post.get('address')
    total = post.get('ototal')
    cart_id = post.getlist('cart_id')
    prices = post.getlist('price')
    # 创建一个新的保存点。这将实现在事物里对“好”的状态做一个标记点。返回值是 savepoint ID (sid).
    sid = transaction.savepoint()
    try:
        carts = MyCart.objects.filter(id__in=cart_id)
        # 判断库存
        for i in carts:
            # 如果库存足够，减少库存
            print i.goods_id.gkucun
            print i.count
            if i.goods_id.gkucun >= i.count:
                i.goods_id.gkucun = F('gkucun') - i.count
                i.goods_id.save()
            else:
                transaction.savepoint_rollback(sid)
                return redirect('/user/cart.html')
        # 生成订单
        user_name = request.session.get('user_name', '')
        user = UserInfo.objects.get(uname=user_name)
        odate = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        oid = odate + str(user.id)
        OrderInfo.objects.create(oid=oid, user=user, odate=odate, oaddress=address, ototal=float(total))
        # 生成订单详情
        order = OrderInfo.objects.get(oid=oid)
        print order
        for n, j in enumerate(carts):
            OrderDetail.objects.create(order=order, goods=j.goods_id, count=j.count, price=prices[n])
            # 删除购物车中的数据
            j.delete()
        transaction.savepoint_commit(sid)
        return redirect('/user/user_center_order')
    except Exception, e:
        print e
        transaction.savepoint_rollback(sid)
        return redirect('/user/cart.html')


