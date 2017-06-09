# coding: utf-8
from django.conf.urls import url
import views


urlpatterns = [
    url(r'^index.html$', views.index, name='index'),
    url(r'^detail.html', views.detail, name='detail'),
    url(r'^get_uname$', views.get_uname, name='get_uname'),
    # 第一个分组是type_id类型，第二个分组是分页信息，第三个是排序信息
    url(r'^lists(\d+)/(\d+)/(order\d)', views.lists, name='lists'),
    url(r'^detail(\d+)', views.detail, name='detail'),
    url('^search', views.MySearchView()),
    url(r'^$', views.index),
]