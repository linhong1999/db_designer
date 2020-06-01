
from django.db import models
import django.utils.timezone as tz
# Create your models here.
#静态表 相当于教务
class Depart(models.Model):#学院
    dNo = models.CharField(max_length=5,primary_key=True) #学院编号
    dName = models.CharField(max_length=5,unique=True) #学院名称
    dSubTime = models.DateTimeField(default=tz.now)
    dDean = models.CharField(max_length=20)#院长
    class Meta:
        db_table = 'Depart'

class DepartMajor(models.Model): #学院院系
    dmNo = models.CharField(max_length=5,primary_key=True)
    dmName = models.CharField(max_length=20,unique=True)
    dmDepart = models.ForeignKey(Depart,models.CASCADE)
    dmSubTime = models.DateTimeField(default=tz.now)#创建日期
    dmDialog = models.TextField() #学院介绍
    dmDeam = models.CharField(max_length=20) #系主任
    class Meta:
        db_table = 'DepartMajor'

class TeacherInfo(models.Model):
    tNo = models.CharField(max_length=20,primary_key=True)
    tName = models.CharField(max_length=20)
    tD = models.ForeignKey(Depart,models.CASCADE)
    tDM = models.ForeignKey(DepartMajor,on_delete=models.CASCADE)
    tRank = models.CharField(max_length=10,choices=(('0','助教'),
                                      ('1','讲师'),
                                      ('2','副教授'),
                                      ('3','教授'),))
    tSalary = models.CharField(max_length=6)
    tDate = models.DateTimeField(default=tz.now) #入职年份

    class Meta:
        db_table = 'Teacher'

class CourseInfo(models.Model):
    COURSE_TYPE = (('0', 'A'), ('1', 'B'), ('2', 'C'), ('3', 'D'))
    #课程编号
    ciNo = models.CharField(max_length=20,primary_key=True)
    ciName = models.CharField(max_length=20)
    ciType = models.CharField(max_length=10, choices=COURSE_TYPE) #课程类型
    #与专业一对多
    ciD = models.ForeignKey(Depart,models.CASCADE)#所属学院
    ciDM = models.ForeignKey(DepartMajor,models.CASCADE)#所属专业
    ciScore = models.CharField(max_length=10,null=True)
    ciCapacity = models.CharField(max_length=10,null=True)
    #ciTeacher = models.ForeignKey(TeacherInfo, models.CASCADE)#课程教师
    ciTerm = models.CharField(max_length=20,default='0')#学期
    #教师通过申请，管理员赋予权力
    #初始为一些基本课程
    class Meta:
        db_table = 'CourseInfo'

class ClassRoomInfo(models.Model):
    BUILDING_NUM_TUPLE = (('0','教1'),('1','教2'),('2','教3'))
    criBuildingNum = models.CharField(max_length=10,choices=BUILDING_NUM_TUPLE)
    criRoomNum = models.CharField(max_length=10)
    criStatus = models.CharField(max_length=5,choices=(('0','占用'),('1','未占用')))

    class Meta:
        db_table = 'ClassRoomInfo'