from django.urls import path,re_path

from Buyer.views import *

urlpatterns = [
    path('base/', base),
    path('index/', index),
    path('register/', register),
    path('login/', login),
    path('logout/', logout),
    path('register_email/', register_email),
    path('sendMessage/', sendMessage),
    re_path('goods_details/(?P<goods_id>\d+)/', goods_details),
    re_path('carJump/(?P<goods_id>\d+)/', carJump),
    path('carList/', carList),
    re_path('delete_goods/(?P<goods_id>\d+)/', delete_goods),
    path('clear_goods/', clear_goods),
    path('addAddress/',addAddress),
    path('address/',address),
    path('enter_order/', add_order),
    re_path('changeAddress/(?P<id>\d+)/', changeAddress),
    re_path('delAddress/(?P<id>\d+)/', delAddress),

    path('openstore/',openstore),

    path('welcome/',welcome),
    re_path('dingdan/(?P<order_num>\d+)',dingdan),

]