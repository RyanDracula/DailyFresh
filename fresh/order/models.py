# coding=utf-8
from goods.models import GoodsInfo
from users.models import UserInfo
from django.db import models

# Create your models here.


class OrderInfo(models.Model):
    """订单信息表"""
    oid = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey(UserInfo)
    odate = models.DateTimeField(auto_now_add=True)
    oIsPay = models.BooleanField(default=False)
    oaddress = models.CharField(max_length=150)
    # 实际支付的总价，最大数目的数字６位，精确到小数点后２位
    ototal = models.DecimalField(max_digits=6, decimal_places=2)


class OrderDetail(models.Model):
    """详细订单（货品信息）"""
    order = models.ForeignKey(OrderInfo)
    goods = models.ForeignKey(GoodsInfo)
    count = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
