from django.db import models
import django.utils.timezone as tz
from django.contrib.auth.models import User

IDEN_TUPLE = (('0', '学生'), ('1', '教师'), ('2', '教务'),('3','root'))
class OperateLog(models.Model):
    DOWHAT_TUPLE = (('0','增加了'),
                    ('1','删除了'),
                    ('2','查找了'),
                    ('3','修改了'),
                    ('4','登陆了'))
    REVIEW_TUPLE = (('0','默认'),('1','通过'),('2','未通过'))
    who = models.CharField(max_length=50)
    iden = models.CharField(max_length=10,choices=IDEN_TUPLE)
    dowhat = models.CharField(max_length=50,choices=DOWHAT_TUPLE)
    detail = models.CharField(max_length=100,null=True,blank=True)
    #审核状态
    review_status = models.CharField(max_length=10,default='0',choices=REVIEW_TUPLE)
    submit_time = models.DateTimeField(default=tz.now)

    class Meta:
        db_table = 'OperateLog'

class LoginInfo(models.Model):
    lNo = models.CharField(max_length=20,primary_key=True)
    lIden = models.CharField(max_length=10,choices=IDEN_TUPLE)
    lPwd = models.CharField(max_length=10,default='000000')
    class Meta:
        db_table = 'LoginInfo'

class LoginLog(models.Model):
    login_ip = models.CharField(max_length=50)
    login_iden = models.CharField(max_length=10,choices=IDEN_TUPLE)
    loginer = models.ForeignKey(LoginInfo,on_delete=models.CASCADE)
    login_time = models.DateTimeField(default=tz.now)
    class Meta:
        db_table = 'LoginLog'
# Create your models here.
