from django.conf.urls import url
import views

urlpatterns = [
    url(r'^register.html/$', views.register, name='register'),
    url(r'^login.html/$', views.login, name='login'),
    url(r'^verify_name', views.verify_name),
    url(r'^verify_email', views.verify_email),
    url(r'^handle_register/$', views.handle_register),
    url(r'^go_login/$', views.go_login),
    url(r'^logout/$', views.logout),
    url(r'^get_site/$', views.get_site),
    url(r'^cart.html/$', views.cart, name='cart'),
    url(r'^add_cart(\d+)/(\d+)', views.add_cart, name='add_cart'),
    url(r'^add_minus$', views.add_minus, name='add_minus'),
    url(r'^user_center_site.html$', views.user_center_site, name='user_center_site'),
    url(r'^user_center_order(\d+)?$', views.user_center_order, name='user_center_order'),
    url(r'^user_center_info.html$', views.user_center_info, name='user_center_info'),
]
