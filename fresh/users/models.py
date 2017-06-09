from django.db import models
from goods.models import GoodsInfo


# Create your models here.
class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    # sha1 encrypt length 40; md5 encrypt length 32;
    upwd = models.CharField(max_length=40)
    email = models.EmailField(max_length=30)


class AdrressInfo(models.Model):
    person = models.CharField(max_length=20)
    addr = models.CharField(max_length=150)
    youbian = models.CharField(max_length=8, default="")
    tel = models.CharField(max_length=20)
    user = models.ForeignKey('UserInfo')


class MyCart(models.Model):
    count = models.IntegerField()
    per_id = models.ForeignKey(UserInfo)
    goods_id = models.ForeignKey(GoodsInfo)



