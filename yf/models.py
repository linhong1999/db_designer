from django.db import models

from yhn.models import DepartMajor,TeacherInfo
from yzk.models import Course
from hg.models import Student
# Create your models here.
COURSE_TYPE = (('0', 'A'), ('1', 'B'), ('2', 'C'), ('3', 'D'))
#忘记和课程得表做关系了
class TeacherOpenCourse(models.Model):
    tocTeacher = models.ForeignKey(TeacherInfo,models.CASCADE)
    tocType = models.CharField(max_length=10, choices=COURSE_TYPE) #课程类型
    tocCapacity = models.CharField(max_length=10,null=True) #课程容量
    tocCName = models.CharField(max_length=20)
    tocScore = models.CharField(max_length=10) #课程学分
    tocStatus = models.CharField(max_length=10,choices=(('0','开放'),('1','待审核')))
    tocOpenTime = models.CharField(max_length=100,null=True)
    tocTerm = models.CharField(max_length=100,null=True) #bei zhu
    class Meta:
        db_table = 'TeacherOpenCourse'

class StudentsChoice(models.Model):
    cCNo = models.ForeignKey(Course,models.CASCADE)
    cStuNo = models.ForeignKey(Student,models.CASCADE)
    cType = models.CharField(max_length=10, choices=COURSE_TYPE) #课程类型
    cTeacher = models.ForeignKey(TeacherInfo,models.CASCADE)
    cGrade = models.CharField(max_length=10,null=True,blank=True)
    cStatus = models.CharField(max_length=10,choices=(('0','重修'),('1','通过'),('2','退选'),('3','未选'),('4','默认')))

    class Meta:
        db_table = 'StudentsChoice'

