from django.db import models
import django.utils.timezone as tz

class TeacherSelectView(models.Model):
    number = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    rank = models.CharField(max_length=20)
    salary = models.CharField(max_length=20)
    date = models.DateTimeField(default=tz.now)

    depart_major = models.CharField(max_length=20) #系
    depart_Deam = models.CharField(max_length=20) #系主任
    depart = models.CharField(max_length=20) #学院
    deam = models.CharField(max_length=20) #院长

    class Meta:
        db_table = 'TeacherSelectView'

#教师查看自己开课情况
class TeacherSelectCourseView(models.Model):
    tch_number = models.CharField(max_length=20)
    course_no = models.CharField(max_length=20)
    course_type = models.CharField(max_length=20)
    course_name = models.CharField(max_length=20)
    course_score = models.CharField(max_length=10)
    #教室情况
    course_building_num = models.CharField(max_length=10)
    course_room_num = models.CharField(max_length=10)
    #教室占用情况
    course_room_status = models.CharField(max_length=10)
    class Meta:
        db_table = 'TeacherSelectCourseView'

class TeacherCourseInfo(models):
    pass
#返回学生成绩信息
#教师查询 教师表时 只能返回自己的信息
#只能返回自己开课的课程信息