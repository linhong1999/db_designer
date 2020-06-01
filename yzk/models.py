from django.db import models
from yhn.models import TeacherInfo, CourseInfo, DepartMajor ,Depart
from hg.models import *
# Create your models here.
class Course(models.Model):
    COURSE_TYPE = (('0','A'),('1','B'),('2','C'),('3','D'))
    cNo = models.ForeignKey(CourseInfo,on_delete=models.CASCADE) #对应课程信息
    cName = models.CharField(max_length=20)
    cDepart = models.ForeignKey(Depart,on_delete=models.CASCADE) #院
    cDepartMajor = models.ForeignKey(DepartMajor,models.CASCADE) #系
    cTerm = models.CharField(max_length=20) #学期
    cCapacity = models.CharField(max_length=3) #课程容量
    cType = models.CharField(max_length=10,choices=COURSE_TYPE)
    cScore = models.CharField(max_length=10) #学分
    cTeacher = models.ForeignKey(TeacherInfo,models.CASCADE)
    #一个课程对应多个教师 一个教师对应多个课程

    class Meta:
        db_table = 'Course'

class CourseInfoList(models.Model):
    COURSE_TYPE = (('0','A'),('1','B'),('2','C'),('3','D'))
    cNo = models.ForeignKey(Course,on_delete=models.CASCADE) #对应课程信息
    cName = models.CharField(max_length=20)
    cDepart = models.ForeignKey(Depart,on_delete=models.CASCADE) #院
    cDepartMajor = models.ForeignKey(DepartMajor,models.CASCADE) #系
    cStudent = models.ForeignKey(Student,models.CASCADE)
    cTerm = models.CharField(max_length=20) #学期
    cCapacity = models.CharField(max_length=3) #课程容量
    cType = models.CharField(max_length=10,choices=COURSE_TYPE)
    cScore = models.CharField(max_length=10) #学分
    cTeacher = models.ForeignKey(TeacherInfo,models.CASCADE)
    cGrade = models.CharField(max_length=10,null=True)
    cPercent = models.CharField(max_length=10,null=True)
    cStatus = models.CharField(max_length=10,null=True,choices=(('0','重修'),('1','通过'),('2','退选'),('3','未选'),('4','默认')))
    #一个课程对应多个教师 一个教师对应多个课程

    class Meta:
        db_table = 'CourseInfoList'

