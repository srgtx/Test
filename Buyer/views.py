from django.shortcuts import render
from Buyer.models import *
from django.shortcuts import HttpResponseRedirect,HttpResponse
from Seller.views import setPassword
from Seller.models import Goods
from django.core.mail import EmailMultiAlternatives
import datetime,random
import time


def base(requset):
    return render(requset,'buyer/base.html',locals())

def cookVaild(fun):
    def inner(request,*args,**kwargs):
        cookier=request.COOKIES
        username=cookier.get('username')
        session=request.session.get("username")
        user = Buyer.objects.filter(username = username).first()
        if  user and session == username:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/buyer/login/")
    return inner

def logout(request):
    response = HttpResponseRedirect("/buyer/login/")
    response.delete_cookie("user_name")
    response.delete_cookie("user_id")
    del request.session["username"]
    return response
@cookVaild
def openstore(request):
    result={'status':'error','data':''}
    user=request.COOKIES.get('username')
    if request.method=="POST" and request.POST:
        username=user


    return render(request,'buyer/openstore.html',locals())

def welcome(request):
    return render(request,'buyer/welcome.html')

@cookVaild
def index(request):
    data=[]
    goods=Goods.objects.all()
    for good in goods:
        goods_img=good.image_set.first()
        if goods_img:
            img=goods_img.img_adress.url
            img = img.replace("/media/","/static/")
        else:
            img = "/static/buyer/image/1.jpg"
        data.append(
            { 'id':good.id,'img':img.replace("media","static"),'name':good.goods_name,'price':good.goods_now_price}
        )

    return render(request,'buyer/index.html',{'datas':data})

def login(request):
    result = {"statue": "error","data": ""}
    if request.method=='POST' and request.POST:
        username=request.POST.get('username')
        user=Buyer.objects.filter(username=username).first()
        if user:
            password=setPassword(request.POST.get('userpass'))
            if password==user.password:
               response= HttpResponseRedirect('/buyer/index')
               response.set_cookie('username',user.username)
               response.set_cookie('user_id',user.id)
               request.session['username']=user.username
               return response
            else:
                result["data"] = "密码错误"
        else:
            result["data"] = "用户名不存在"
    return  render(request,'buyer/login.html',{'result':result})
def register(request):
    if request.method=='POST' and request.POST:
        username=request.POST.get('username')
        password=request.POST.get('userpass')
        buyer=Buyer()
        buyer.username=username
        buyer.password=setPassword(password)
        buyer.save()
        return HttpResponseRedirect('/buyer/login')
    return render(request,'buyer/register.html',locals())

def getRandom():
    result=str(random.randint(1000,9999))
    return result

def sendMessage(request):
    result={'statu':'error','data':''}
    if request.method=='GET' and request.GET:
        recver=request.GET.get('email')
        try:
            subject="验证码"
            text_content='hello word'
            value=getRandom()
            html_content="""
            <div>
                <p>
                    尊敬的q商城用户，您的用户验证码是:%s,请切勿向他人泄露，以防止上当受骗
                </p>
            </div>
            """%value
            message=EmailMultiAlternatives(subject,text_content,'18203640558@163.com',[recver])
            message.attach_alternative(html_content,'text/html')
            message.send()
        except Exception as e:
            result['data']=str(e)
        finally:
            return HttpResponse(result)


def register_email(request):
    result={'statu':'error','data':''}
    if request.method=="POST" and request.POST:
        username=request.POST.get('username')
        code = request.POST.get('code')
        password=request.POST.get("userpass")
        user=EmailVaild.objects.filter(email_address=username).first()
        if user:
            if code==user.value:
                now=time.mktime(
                    datetime.datetime.now().timetuple()
                )
                db_now=time.mktime(user.times.timetuple())
                if now-db_now>=86400:
                    result["data"]='验证码以过期'
                    user.delate()
                else:
                    buyer=Buyer()
                    buyer.username=username
                    buyer.email=username
                    buyer.password=setPassword(password)
                    buyer.save()
                    result["data"]='注册成功'
                    result["statu"] = "success"
                    user.delate()
                    return HttpResponseRedirect('/buyer/login')
            else:
                result["data"]='验证码错误'
        else:
            result["data"]="验证码不存在"

    return render(request,'buyer/register_email.html')

def goods_details(request,goods_id):
    good=Goods.objects.get(id=int(goods_id))
    types=good.types
    seller=good.seller
    img=good.image_set.first()
    goods=seller.goods_set.all()[:4]
    goods_list=[]
    for g in goods:
        goods_img=g.image_set.first()
        goods_list.append(
            {'id':g.id,'name':g.goods_name,'price':g.goods_now_price,'img':goods_img}
        )

    return render(request,'buyer/goods_details.html',locals())

def carJump(request,goods_id):     #goods_id是自增的那个id
    user_id=request.COOKIES.get("user_id")
    goods_id=int(goods_id)
    goods=Goods.objects.get(id=goods_id)
    if request.method=="POST" and request.POST:
        count=int(request.POST.get('count'))
        img=request.POST.get('goods_img')

        buycar=BuyCar.objects.filter(goods_id=goods_id,user_id=user_id).first()
        if not buycar:
            buycar=BuyCar()
            buycar.goods_num=count
            buycar.goods_id=goods_id
            buycar.goods_name=goods.goods_name
            buycar.goods_picture=img
            buycar.goods_price=goods.goods_now_price
            buycar.user=Buyer.objects.get(username=request.COOKIES.get('username'))
            buycar.save()
        else:
            buycar.goods_num+=count
            buycar.save()
        all_price=float(buycar.goods_price*count)
        return render(request,'buyer/buyCar_jump.html',locals())
    else:
        return HttpResponse('404')


def carList(request):
    user_id=request.COOKIES.get('user_id')
    buyCar=BuyCar.objects.filter(user=user_id)
    addr=Address.objects.filter(buyer_id=user_id)
    good_list=[]
    for goods in buyCar:
        all_price=format(float(goods.goods_price)*int(goods.goods_num),'.2f')
        good_list.append({'all_price':all_price,'goods':goods})
    return render(request,'buyer/car_list.html',locals())

@cookVaild
def delete_goods(request,goods_id):
    id=request.COOKIES.get('user_id')

    goods=BuyCar.objects.filter(user = int(id),goods_id = int(goods_id)).first()

    goods.delete()

    return HttpResponseRedirect("/buyer/carList/")
@cookVaild
def clear_goods(request):
    id=request.COOKIES.get('user_id')
    goods=BuyCar.objects.filter(user_id=int(id))
    goods.delete()

    return HttpResponseRedirect("/buyer/carList/")

def addAddress(request):

    if request.method=='POST' and request.POST:
        id=request.COOKIES.get("user_id")
        buyer=request.POST.get('buyer')
        buyer_phone=request.POST.get('buyer_phone')
        buyer_address=request.POST.get('buyer_address')
        db_buyer = Buyer.objects.get(id = int(id))
        addr=Address()
        addr.recver=buyer
        addr.phone=buyer_phone
        addr.address=buyer_address
        addr.buyer=db_buyer
        addr.save()
        return HttpResponseRedirect("/buyer/address/")
    return render(request,'buyer/addAddress.html')

def address(request):
    id=request.COOKIES.get("user_id")
    address_list=Address.objects.filter(buyer=id)
    return render(request,'buyer/address.html',locals())
def changeAddress(request,id):
    user_id=request.COOKIES.get('user_id')
    addr=Address.objects.get(id=int(id))
    if request.method=='POST' and request.POST:
        buyer=request.POST.get('buyer')
        buyer_phone=request.POST.get('buyer_phone')
        buyer_address=request.POST.get('buyer_address')

        addr.recver=buyer
        addr.phone=buyer_phone
        addr.address=buyer_address
        addr.save()
        return HttpResponseRedirect("/buyer/address/")
    return render(request,'buyer/addAddress.html',locals())

def delAddress(request,id):
    addr=Address.objects.filter(id=int(id)).first()
    addr.delete()
    return HttpResponseRedirect("/buyer/address/")

def add_order(request):
    buy_id=request.COOKIES.get('user_id') # 用户ID
    goods_list=[]   #商品列表
    if request.method=='POST' and request.POST:
        requestData = request.POST #请求数据
        addr =requestData.get('address') #寄送地址的id
        pay_method = requestData.get("pay_Method") #支付方式
        all_price=0.00
        for key,value in requestData.items():
            if key.startswith("name"):#如果键以name开头，我们就任务是一条商品信息的id
                buyCar=BuyCar.objects.filter(id=int(value)).first()  #获取商品
                price = buyCar.goods_num * float(buyCar.goods_price) #单条商品的总价
                all_price+=price
                goods_list.append({"price":price,"buyCar":buyCar}) #构建数据模型{"小计总价":price,"商品信息":buyCar}

        # 存入订单库
        addr=Address.objects.get(id=int(addr)) #获取地址数据
        order = Order() #保存到订单
        now = datetime.datetime.now()
        order.order_num=now.strftime("%Y%m%d")+str(random.randint(1000,9999))
        order.order_time=now
        # 状态 未支付 1 支付成功 2 配送中 3 交易完成 4 已取消 0
        order.order_statue = 1
        order.total = all_price
        order.user=Buyer.objects.get(id=buy_id)
        order.order_address=addr
        order.save()
        order.order_num=order.order_num+str(order.id)
        order.save()

        for good in goods_list:
            g = good["buyCar"]
            g_o = OrderGoods()
            g_o.goods_id = g.id
            g_o.goods_name=g.goods_name
            g_o.goods_price = g.goods_price
            g_o.goods_num = g.goods_num
            g_o.goods_picture = g.goods_picture
            g_o.order = order
            g_o.save()
        return render(request,"buyer/enterOrder.html",locals())
    else:
        return HttpResponseRedirect("/buyer/carList")


from alipay import AliPay
def dingdan(request,order_num):

    order=Order.objects.get(order_num=order_num)
    alipay_public_key_string = '''-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvm6rwpqTphs5xKrFDZ1YE5h6vsh48+ERfZ4p5SQ2woYot4XQykmy91mN7bjXgGdyO5gTT0Dtc7jvzb4fcVwVC46Dc7KiRgnXULdc3bTEpSjL2acr+AfLcek/KLquv6wXg4rVFWbm6eFI+3gxUaq21n8PLSLt2y0870jY6fxx7h5HBKatI6z30rKpx8AWqGsoCpwYITwUJnaJrkxFD/VFsZT+A2VIVEHBTwM8/iHqsIS9ZlUTzaUMZBWgGCZD4moy1YNvDrDShrGw/7PfhhuLHMZFo7zfhLy8PDABBjXhZ7eY4aPa3OyWL9yaUfcBdRpIhO6jlmBiPUF6hPKVwVf8xwIDAQAB
-----END PUBLIC KEY-----'''

    app_private_key_string = '''-----BEGIN RSA PRIVATE KEY-----
    MIIEpQIBAAKCAQEAvm6rwpqTphs5xKrFDZ1YE5h6vsh48+ERfZ4p5SQ2woYot4XQykmy91mN7bjXgGdyO5gTT0Dtc7jvzb4fcVwVC46Dc7KiRgnXULdc3bTEpSjL2acr+AfLcek/KLquv6wXg4rVFWbm6eFI+3gxUaq21n8PLSLt2y0870jY6fxx7h5HBKatI6z30rKpx8AWqGsoCpwYITwUJnaJrkxFD/VFsZT+A2VIVEHBTwM8/iHqsIS9ZlUTzaUMZBWgGCZD4moy1YNvDrDShrGw/7PfhhuLHMZFo7zfhLy8PDABBjXhZ7eY4aPa3OyWL9yaUfcBdRpIhO6jlmBiPUF6hPKVwVf8xwIDAQABAoIBAQCqDHWALzxNhd5OChgwkiKGTRC+sJGhZYeS3tuWbIIhrl9JkkrheHJBgkzEzNxTIwzUvnXvvZDMV4Z7+JxnQ8zfJwGnHQre9Aa7YyGgML2wpf9yel8++ubm71ug6SMGsYvFwQGKPPtSOgRL2gZgYMsoOwm4SoqPv5O8MRbRysWJ1SFFJPenmsVqbcEJfIgeZWPMahVYlwRr/S4hR5vscFPVF0R5Pk7+JAN9zBbNKXg8bpYsm+CQU11PY2PyeRkletkcxFcwR2Z1c4Kn90Vm7WNINQ2iPoC0LlMAYozVdRVYPF+On4JFeHM93f6uPAS6gh9PPfS3f/9jhBP64u8D1ekhAoGBAN+fwY/2yOA0JhuupR2u6bz0kfxmUFi1i6kRYUbcF+NGcDnoRp/iVBVrDkhOFDr8mEoNV/bbExqfR+aeKH7eya2mYPVU2MOh1gNh0qywM8i9nj0REUNlwEzjm4Eaj0zqJ4Ss4oxbdpwDNK7uqgcGIMgp+he7ImI/SVcTTbS/l1LfAoGBANoAuDqYYKCsa2qx3vCQHD7sOrEUKo2gslm/WsNSmS+d1GIvxbmVAcKqHrzY212YZ6huLZ7MCl149y3xF/BlrOWz/QEe0hIcHbARlWAFwg8/5TFoKLtRAepRE1XLdsyQl8Cosutt8qCwmcLupjZX4ffA6uNEvcyafQ2aQs4G+LsZAoGBAKI9KlZDKiuXSgqNY1esvgGLwppGtIYXeHK5nESni2ElimhIv2xh7LT5TYxhsUW2Wtpm4enDuRF4e9ax6hlZkyI78l4rJ3SPZlBf2VPWJku+Xh5Z0pd+K8zc2MYKueqIexFDyL0h4mR/4uoDVzHvXTs7USmEaAa1eYUGCTtYQPYrAoGBAIAlhCYNhF9uewYQ4LgQPkpOmoGVFR6Do9NVxIikeR+ga0P8SQI6MPq4/bCM2QY/nE9J1M9PqZggj0wWOLg7TFMKZmLONzYmCN2CuIflWpmUOam9TJQvniya0/7Ox1qgdFPv1pzF2KXUqc4IcvPm3RHB+VD3C4rGFVR1pWduea+hAoGAeo4l597OAsz+ZmsEDDkY99bD8FKjt816AWDbyDKi5woL0jiRFA/TZszt0nhz4Q+qTBHV5X3ImMjHbdsJ9e6FadBbZM5YgPXdOthRz3AKJyF4oLh3D3GfsszzxUD1wEz+Z3S2/n/YQP8CxjbrDvOapR+gR/0F/TKSakO/Yzq/DKo=
-----END RSA PRIVATE KEY-----'''

#如果在Linux下，我们可以采用AliPay方法的app_private_key_path和alipay_public_key_path方法直接读取.emp文件来完成签证
#在windows下，默认生成的txt文件，会有两个问题
#1、格式不标准
#2、编码不正确 windows 默认编码是gbk

#实例化应用
    alipay = AliPay(
        appid="2016092400586019", #支付宝app的id
        app_notify_url=None, #会掉视图
        app_private_key_string = app_private_key_string, #私钥字符
        alipay_public_key_string = alipay_public_key_string, #公钥字符
        sign_type="RSA2", #加密方法
    )
#发起支付
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_num,
        total_amount=order.total,  # 将Decimal类型转换为字符串交给支付宝
        subject="商贸商城",
        return_url="http://127.0.0.1:8000/buyer/index",
        notify_url=None  # 可选, 不填则使用默认notify url
)

# 让用户进行支付的支付宝页面网址
    return   HttpResponseRedirect("https://openapi.alipaydev.com/gateway.do?"+order_string)
# Create your views here.
