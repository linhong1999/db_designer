from django.db import models
from yhn.models import DepartMajor, TeacherInfo, Depart
import django.utils.timezone as tz
# Create your models here.
class Student(models.Model):
    sNo = models.CharField(max_length=20, primary_key=True)
    sName = models.CharField(max_length=20)
    sSex = models.CharField(max_length=10,choices=(('0', 'female'), ('1', 'male')))  # 0 女生 1 男生
    sD = models.ForeignKey(Depart, models.CASCADE)#院
    sDM = models.ForeignKey(DepartMajor, on_delete=models.CASCADE) #系
    s_mentor = models.ForeignKey(TeacherInfo, models.CASCADE)  # 外键教师
    sYear = models.CharField(max_length=20,null=True) #入学年份
    class Meta:
        db_table = 'Student'

class StudentClass(models.Model):
    scSNo = models.ForeignKey(Student, models.CASCADE)  # 学生学号
    scDM = models.ForeignKey(DepartMajor, models.CASCADE) #系   候选码1
    scD = models.ForeignKey(Depart, models.CASCADE)  #院   候选码2
    scNo = models.CharField(max_length=20)  # 班级编号 171 172 181 182...  候选码2

    class Meta:
        db_table = 'StudentClass'

