from django.db import models
import django.utils.timezone as tz

#学生查询自己信息
class StuSelectInfoView(models.Model):
    number = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    sex = models.CharField(max_length=10)
    class_num = models.CharField(max_length=20)    #班级
    mentor = models.CharField(max_length=20)       #导师
    year = models.DateTimeField(default=tz.now)

    depart_major = models.CharField(max_length=20) #系
    depart_Deam = models.CharField(max_length=20) #系主任
    depart = models.CharField(max_length=20) #学院
    deam = models.CharField(max_length=20) #院长

    class Meta:
        db_table = 'StuSelectInfoView'

#学生查询选课情况
# 根据学生的学号 能 唯一确定一个学生的信息
# 能 从 选课情况表中获取所有 此 学生的选课情况
class StuSelectCourseInfo(models.Model):
    course_num = models.CharField(max_length=20)
    course_name = models.CharField(max_length=20)
    grade = models.CharField(max_length=3)
    status = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    date = models.CharField(max_length=20) #选修时间

    course_score = models.CharField(max_length=3) #学分
    avg = models.CharField(max_length=20) #平均分
    top = models.CharField(max_length=20) #最高分
    min = models.CharField(max_length=20) #最低分

    class Meta:
        db_table = 'StuSelectCourseInfo'