from alipay import AliPay

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
    out_trade_no="32454161",
    total_amount=str(1),  # 将Decimal类型转换为字符串交给支付宝
    subject="商贸商城",
    return_url="",
    notify_url=None  # 可选, 不填则使用默认notify url
)

# 让用户进行支付的支付宝页面网址
print("https://openapi.alipaydev.com/gateway.do?"+order_string)