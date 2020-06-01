from django.db.models import Q
from django.shortcuts import render, redirect
from yzk.models import Course, CourseInfoList
from lh.views import operate_log, CourseInfo
from yf.models import *
from .models import *
# Create your views here.
def StuAddCourseHtml(req):
    #A类是基础的 为学生自动选上的
    #当教师添加了一个学生之后
    #自动补全学生在该专业的所有必修课程
    #别的是选修的，学生手动选择的
    no = req.session['lNo']
    #已选但 可能未选教师
    already_choosed = StudentsChoice.objects.filter(cStatus='3',cStuNo_id=req.session['lNo'])
    same_tch_list = Course.objects.filter(cType='0').values('cName','cDepartMajor','cDepart').values_list('cTeacher','cName')
    #B类为专业必修类 若B类课程所属专业和学生专业不一样
    #则自动归为 C类 院选类
    #选出本专业开放的所有课程
    # B_opened = TeacherOpenCourse.objects.filter(tocTeacher__tNo=Student.objects.get(sNo=no).sDM_id)
    # course = CourseInfoList.objects.filter(cStudent_id=req.session['lNo'])
    aaa = []
    ccc = []
    ddd = []
    for course in CourseInfoList.objects.filter(cStudent_id=req.session['lNo']):
        ddd.append({'course':course,'remaining':len(CourseInfoList.objects.filter(cNo_id=course.cNo_id))})
    stu = Student.objects.get(sNo=req.session['lNo'])
    # B_opened = Course.objects.filter(cDepart_id=stu.sD_id,cDepartMajor_id=stu.sDM_id,cType='1')
    for course in Course.objects.filter(cDepart_id=stu.sD_id,cDepartMajor_id=stu.sDM_id,cType='1'):
        aaa.append({'B_opened':course,'remaining':len(CourseInfoList.objects.filter(cNo_id=course.id))})
    # other_opened = Course.objects.filter(~Q(cDepartMajor_id=stu.sDM_id))
    for course in Course.objects.filter(~Q(cDepartMajor_id=stu.sDM_id)&~Q(cType='0')):
        ccc.append({'other_opened':course,'remaining':len(CourseInfoList.objects.filter(cNo_id=course.id))})
    return render(req,'stu_add_course.html',{
        'already_choosed':already_choosed,'B_opened':aaa,
        'other_opened':ccc,'same_tch_list':same_tch_list,
        'courses':ddd
    })
# @operate_log(('添加了','选修课'))
def StuAddCourse(req):
    StudentsChoice.objects.filter(cCNo_id=req.GET.get('cCNo'),cStuNo_id=req.session['lNo']).update(cTeacher_id=req.GET.get('cTeacher'),cStatus='4')
    #     cCNo=Course.objects.get(cNo=req.GET.get('cCNo')),
    #     cStuNo=Student.objects.get(sNo=req.session['cStuNo']),
    #     cTeacher=TeacherInfo.objects.get(tNo=req.GET.get('cTeacher'))
    # )
    obj = Course.objects.get(id=req.GET.get('cCNo'))
    CourseInfoList.objects.create(
        cNo=obj,cName=obj.cName,cDepart=obj.cDepart,cDepartMajor=obj.cDepartMajor,
        cStudent=Student.objects.get(sNo=req.session['lNo']),cTerm=obj.cTerm,
        cCapacity=obj.cCapacity,cType=obj.cType,cScore=obj.cScore,cTeacher=TeacherInfo.objects.get(tNo=req.GET.get('cTeacher')),
        cStatus='4'
    )
    return redirect('/stu_add_course_html/')

def StuDelCourse(req):
    if Course.objects.get(id=req.GET.get('cCNo')).cType == '0':
        StudentsChoice.objects.filter(cCNo_id=req.GET.get('cCNo'), cStuNo_id=req.session['lNo']).update(cStatus='3',cTeacher_id='1002')
    else:
        StudentsChoice.objects.filter(cCNo_id=req.GET.get('cCNo'), cStuNo_id=req.session['lNo']).delete()
    CourseInfoList.objects.filter(cStudent_id=req.session['lNo'], cNo_id=req.GET.get('cCNo')).delete()

    return redirect('/stu_add_course_html/')