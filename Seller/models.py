from django.db import models



class Types(models.Model):
    label = models.CharField(max_length=32)
    parent_id=models.IntegerField()
    description=models.TextField()

class Seller(models.Model):
    username=models.CharField(max_length=32)
    password=models.CharField(max_length=32)
    nickname=models.CharField(max_length=32)  #真实名字
    photo=models.ImageField(upload_to='image')
    phone=models.CharField(max_length=32)
    address=models.CharField(max_length=32)
    email=models.EmailField()
    id_number=models.CharField(max_length=32) #身份证号

class Goods(models.Model):
    goods_id=models.CharField(max_length=32)
    goods_name=models.CharField(max_length=32)
    goods_price=models.FloatField()        #原价
    goods_now_price=models.FloatField()    #当前价格
    goods_num=models.IntegerField()        #库存
    goods_description=models.TextField()   #描述
    goods_content=models.TextField()       #详情


    types=models.ForeignKey(Types,on_delete=True)
    seller = models.ForeignKey(Seller,on_delete=True)

class Image(models.Model):
    img_adress = models.ImageField(upload_to = "image")
    img_label = models.CharField(max_length = 32)
    img_description= models.TextField()
    goods = models.ForeignKey(Goods,on_delete=True)  # 一个商品多张图片

class BankCard(models.Model):
    number = models.CharField(max_length=32)
    bankAddress = models.CharField(max_length=32)
    username = models.CharField(max_length=32)  # 持卡人姓名
    idCard = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)

    seller = models.ForeignKey(Seller, on_delete=True)
# Create your models here.
