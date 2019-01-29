import smtplib   #smtp 服务器

from email.mime.text import MIMEText

subject='送邮件'
content='子鼠丑牛寅虎卯兔辰龙巳蛇午马未羊申猴酉鸡戌狗亥猪'
sender='18203640558@163.com'
recver='993066119@qq.com'
password='zxc123456'
message=MIMEText(content,'html',"utf-8")

message['Subject'] = subject
message['To'] = recver
message['From']=sender

smtp=smtplib.SMTP_SSL("smtp.163.com",994)
smtp.login(sender,password)
smtp.sendmail(sender,[recver],message.as_string())
smtp.close()