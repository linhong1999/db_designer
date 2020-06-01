from django.http import HttpResponse
from django.shortcuts import render, redirect

from lh.models import LoginInfo
from yzk.models import Course
from .models import *
from lh.views import operate_log
# Create your views here.

def AddDepartHtml(req):
    depart_info = [{
        'dNo':item.dNo,'dName':item.dName,'dDean':item.dDean
    }for item in Depart.objects.all()]
    return render(req,'add_depart.html',{'items':depart_info})

@operate_log('添加了','学院')
def AddDepart(req):
    kwargs = {key:req.POST.get(key) for key in ['dNo','dName','dDean']}
    Depart(**kwargs).save()
    return redirect('/add_depart_html/')

@operate_log('删除了','学院')
def DelDepart(req):
    Depart.objects.filter(dNo=req.GET.get('dNo')).delete()
    return redirect('/add_depart_html/')

def AddDepartMajorHtml(req):
    depart_major_info = [{
        'dmNo':item.dmNo,'dmName':item.dmName,'dmDepart':item.dmDepart.dName,
        'dmDialog':item.dmDialog,'dmDeam':item.dmDeam,'dmSubTime':item.dmSubTime
    }for item in DepartMajor.objects.all()]
    return render(req,'add_depart_major.html',{'items':depart_major_info})

@operate_log('添加了','系')
def AddDepartMajor(req):
    kwargs = {key:req.POST.get(key) for key in ['dmNo','dmName','dmDepart','dmDialog','dmDeam']}
    kwargs['dmDepart'] = Depart.objects.get(dNo=kwargs['dmDepart'])
    DepartMajor.objects.create(**kwargs)
    return redirect('/add_depart_major_html/')

@operate_log('删除了','系')
def DelDepartMajor(req):
    DepartMajor.objects.filter(dmNo=req.GET.get('dmNo')).delete()
    return redirect('/add_depart_major_html/')

def AddTeacherHtml(req):
    teacher_info = [{
        'tNo': item.tNo, 'tName': item.tName, 'tDM': item.tDM.dmName,'tD':item.tD.dName,
        'tRank': item.get_tRank_display(), 'tSalary': item.tSalary, 'tDate': item.tDate
    } for item in TeacherInfo.objects.all()]
    return render(req, 'add_teacher.html', {'items': teacher_info})

@operate_log('添加了','教师')
def AddTeacher(req):
    #添加教师之后自动生成登陆账号
    kwargs = {key:req.POST.get(key) for key in ['tNo','tName','tRank','tSalary','tDM','tD']}
    kwargs['tDM'] = DepartMajor.objects.get(dmNo=kwargs['tDM'])
    kwargs['tD'] = Depart.objects.get(dNo=kwargs['tD'])
    TeacherInfo.objects.create(**kwargs)
    LoginInfo(lNo=kwargs['tNo'],lIden='1').save()
    return redirect('/add_teacher_html/')

@operate_log('删除了','教师')
def DelTeacher(req):
    TeacherInfo.objects.filter(tNo=req.GET.get('tNo')).delete()
    return redirect('/add_teacher_html/')

def AddBaseCourseHtml(req):
    teacher_info = [{
        'cNo': item.ciNo, 'cName': item.ciName, 'cTerm': item.ciTerm,
        'cType': item.get_ciType_display(), 'cDepart': item.ciD.dName,'cDepartMajor':item.ciDM.dmName,
        'cCapacity':item.ciCapacity,'cScore':item.ciScore,'cTeacher':''
    } for item in CourseInfo.objects.all()]
    return render(req, 'add_base_course.html', {'items': teacher_info})
#基础课程添加后 该院系所有学生都自动选上该门课
#课程容量 课程学分 记得弄
@operate_log('添加了','基础课程')
def AddBaseCourse(req):
    kwargs = {key:req.POST.get(key) for key in ['ciNo','ciTerm','ciName','ciType','ciDM','ciD','ciScore','ciCapacity']}
    kwargs['ciDM'] = DepartMajor.objects.get(dmName=kwargs['ciDM'])
    kwargs['ciD'] = Depart.objects.get(dName=kwargs['ciD'])
    CourseInfo.objects.create(**kwargs)
    Course.objects.create(
        cNo=CourseInfo.objects.get(
            ciNo=kwargs['ciNo']),cName=kwargs['ciName'],cDepart=kwargs['ciD'],
            cDepartMajor=kwargs['ciDM'],cTerm=kwargs['ciTerm'],cCapacity=kwargs['ciCapacity'],
            cType=kwargs['ciType'],cScore=kwargs['ciScore'],cTeacher=TeacherInfo.objects.get(tNo=req.session['lNo'])
    )
    #many to many 这样写 add set 都行
    # obj.cTeacher.add(TeacherInfo.objects.get(tNo=req.session['lNo']))
    # obj.cTeacher.set(TeacherInfo.objects.filter(tNo=req.session['lNo']))
    return redirect('/add_base_course_html/')

@operate_log('删除了','基础课程')
def DelBaseCourse(req):
    CourseInfo.objects.filter(ciNo=req.GET.get('cNo')).delete()
    return redirect('/add_base_course_html/')


# @operate_log(('添加了','可用教室'))
def AddClassRoom(req):
    kwargs = {key:req.POST.get(key) for key in ['criBuildingNum','criRoomNum']}
    ClassRoomInfo(criBuildingNum=kwargs['cirBuildingNum'],criRoomNum=kwargs['criRoomNum'],criStatus=0).save()
    pass