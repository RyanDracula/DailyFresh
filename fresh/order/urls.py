from django.conf.urls import url
import views

urlpatterns = [
    url(r'^place_order', views.place_order, name='place_order'),
    url(r'^submit_order', views.submit_order, name='submit_order'),
]