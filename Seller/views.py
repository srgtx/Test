from django.shortcuts import render
from  Seller.models import *
import hashlib,os
from django.shortcuts import HttpResponseRedirect,HttpResponse
from Qshop.settings import MEDIA_ROOT

def setPassword(password):
    md5=hashlib.md5()
    md5.update(password.encode())
    result=md5.hexdigest()
    return result

def cookierValid(fun):
    def inner(request,*args,**kwargs):
        cookie=request.COOKIES
        session=request.session.get('nickname') #获取session
        user=Seller.objects.filter(username=cookie.get('username')).first()
        if user and session==user.username:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/seller/login')
    return inner

@cookierValid
def goods_list(request):

    goods_list=Goods.objects.all()

    return render(request,'seller/goods_list.html',locals())

@cookierValid
def goods_add(request):
    result={'statue':'error','data':''}
    if request.method=='POST' and request.POST:
        # type_id=Types.objects.filter(label=request.POST.get('goods_type')).first()
        type_id=request.POST.get('goods_type')
        seller_id=Seller.objects.filter(username=request.session.get('nickname')).first()
        goods_id=request.POST.get('goods_num')
        goods_name=request.POST.get('goods_name')
        goods_price=request.POST.get('goods_oprice')
        goods_now_price=request.POST.get('goods_xprice')
        goods_num=request.POST.get('goods_count')
        goods_description=request.POST.get('goods_infro')
        goods_content=request.POST.get('goods_content')
        goods_photo=request.FILES.getlist('userfiles')

        g=Goods()
        g.goods_id=goods_id
        g.goods_name=goods_name
        g.goods_price=goods_price
        g.goods_now_price=goods_now_price
        g.goods_num=goods_num
        g.goods_description=goods_description
        g.goods_content=goods_content
        g.types_id= int(type_id)
        g.seller_id=seller_id.id
        g.save()

        # path=os.path.join(MEDIA_ROOT,'image\\%s'%photo)
        # with open(path,'wb') as f:
        #     for i in goods_photo.chunks(): #解析文件
        #         f.write(i)
        for index,img in enumerate(goods_photo):
            file_name=img.name
            file_path='seller/image/%s_%s.%s'%(goods_name,index,file_name.rsplit('.',1)[1])
            save_path = os.path.join(MEDIA_ROOT,file_path).replace('/','\\')
            try:
                with open(save_path,'wb') as f:
                    for chunk in img.chunks(chunk_size=1024):
                        f.write(chunk)
                i=Image()
                i.img_adress=file_path
                i.img_label='%s_%s'%(index,goods_name)
                i.img_description='this is description'
                i.goods=g
                i.save()
            except Exception as e:
                print(e)
            # i.img_adress=j
            # i.goods_id=g.id
            # i.save()


    return render(request,'seller/goods_add.html',locals())
def login(request):
    result={'statue':'error','data':''}
    if request.method=='POST' and request.POST:
        username=request.POST.get('username')
        user=Seller.objects.filter(username=username).first()
        if user:
            password=setPassword(request.POST.get('password'))
            if password==user.password:
                response=HttpResponseRedirect('/seller/index/')
                response.set_cookie('username',user.username)
                request.session['nickname']=user.username #设置session
                return response
            else:
                result['data']='密码错误'
        else:
            result['data']='用户名错误'

    return render(request,'seller/login.html',{'result':result})

@cookierValid
def index(request):

    return render(request,'seller/index.html',locals())

@cookierValid
def logout(request):
    username=request.COOKIES.get('username')
    if username:
        response=HttpResponseRedirect('/seller/login/')
        response.delete_cookie('username')
        return response
    else:
        return HttpResponseRedirect('/seller/login')

@cookierValid
def goods_del(request,id):

    goods=Goods.objects.get(id=int(id))
    imgs=goods.image_set.all()
    imgs.delete()
    goods.delete()

    return HttpResponseRedirect('/seller/goods_list')

def goods_change(request,id):

    goods=Goods.objects.get(id=int(id))

    if request.method=='POST' and request.POST:
        if request.POST.get('redact'):
            imgs=goods.image_set.all()
            imgs.delete()
            goods.delete()

        # type_id=Types.objects.filter(label=request.POST.get('goods_type')).first()
        type_id=request.POST.get('goods_type')
        seller_id=Seller.objects.filter(username=request.session.get('nickname')).first()
        goods_id=request.POST.get('goods_num')
        goods_name=request.POST.get('goods_name')
        goods_price=request.POST.get('goods_oprice')
        goods_now_price=request.POST.get('goods_xprice')
        goods_num=request.POST.get('goods_count')
        goods_description=request.POST.get('goods_infro')
        goods_content=request.POST.get('goods_content')
        goods_photo=request.FILES.getlist('userfiles')

        g=Goods()
        g.goods_id=goods_id
        g.goods_name=goods_name
        g.goods_price=goods_price
        g.goods_now_price=goods_now_price
        g.goods_num=goods_num
        g.goods_description=goods_description
        g.goods_content=goods_content
        g.types_id= int(type_id)
        g.seller_id=seller_id.id
        g.save()

        # path=os.path.join(MEDIA_ROOT,'image\\%s'%photo)
        # with open(path,'wb') as f:
        #     for i in goods_photo.chunks(): #解析文件
        #         f.write(i)
        for index,img in enumerate(goods_photo):
            file_name=img.name
            file_path='seller/imag/%s_%s.%s'%(goods_name,index,file_name.rsplit('.',1)[1])
            save_path = os.path.join(MEDIA_ROOT,file_path).replace('/','\\')
            try:
                with open(save_path,'wb') as f:
                    for chunk in img.chunks(chunk_size=1024):
                        f.write(chunk)
                i=Image()
                i.img_adress=file_path
                i.img_label='%s_%s'%(index,goods_name)
                i.img_description='this is description'
                i.goods=g
                i.save()
            except Exception as e:
                print(e)
        return HttpResponseRedirect('/seller/goods_list')


    return render(request,'seller/goods_add.html',locals())



# Create your views here.
# def example(request):
#     s=Seller()
#     s.username='admin'
#     s.password=setPassword('admin')
#     s.nickname='衣衣不舍'
#     s.photo='imag/11.jpg'
#     s.phone=18329785739
#     s.address='上海'
#     s.email='yiyibushe@qq.com'
#     s.id_number=413529199906074762
#     s.save()
#
#
#     return render(request,'seller/example.html',locals())