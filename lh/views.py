from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from hg.models import *
from yhn.models import *
from yf.models import *
from yzk.models import *
# Create your views here.
REDIRECT_DIC = {
    '0':'/stu_add_course_html/',
    '1':'/teacher_add_course_html/',
    '2':'/add_depart_html/',
    '3':'/release_html/'
}
def operate_log(*args):
    def wrapper(func):
        def log(req):
            try:
                OperateLog(who=req.session['lNo'],iden=req.session['lIden'],
                            dowhat=args[0],detail=args[1],review_status='0').save()
                return func(req)
            except Exception as err:
                return HttpResponse(err)
        return log
    return wrapper

def login_log(req):
    if 'HTTP_X_FORWARDED_FOR' in req.META:  # 获取 ip
        client_ip = req.META['HTTP_X_FORWARDED_FOR']
    #    print(client_ip)
        client_ip = client_ip.split(",")[0]  # 真实 ip
    else:
        client_ip = req.META['REMOTE_ADDR']
    LoginLog.objects.create(
         login_ip=client_ip,
         login_iden=req.POST.get('lIden'),
         loginer=LoginInfo.objects.get(lNo=req.POST.get('lNo'))
         )
    return HttpResponse('success')
    pass

def login(req):
    login_log(req)
    iden = req.POST.get('lIden')
    no = req.POST.get('lNo')
    if LoginInfo.objects.filter(lNo=no,lIden=iden,lPwd=req.POST.get('lPwd')):
        req.session['lIden'] = iden
        req.session['lNo'] = no
        return redirect(REDIRECT_DIC[iden])
    else:
        return HttpResponse('error')


def ReleaseHtml(req):
    tch_open_course = TeacherOpenCourse.objects.filter(tocStatus='1')
    login_log_list = LoginLog.objects.all()
    operate_log_list = OperateLog.objects.all()
    return render(req,'release.html',{
        'tch_open_course':tch_open_course,
        'login_log_list':login_log_list,
        'operate_log_list':operate_log_list,
    })
def Release(req,id):
    import time
    course = TeacherOpenCourse.objects.filter(id=id)
    course.update(tocStatus='0')
    course=course[0]
    obj = CourseInfo.objects.filter(ciName=course.tocCName)
    if obj:
        obj=obj[0]
        Course(
            cNo=obj, cName=obj.ciName, cDepart=obj.ciD, cDepartMajor=obj.ciDM,
            cTerm=obj.ciTerm, cCapacity=obj.ciCapacity, cType=obj.ciType,
            cScore=obj.ciScore, cTeacher=TeacherInfo.objects.get(tNo=course.tocTeacher_id)
        ).save()
    else:
        #用时间戳加教师编号做唯一
        obj = CourseInfo(
            ciNo=str(course.tocTeacher_id)+str(time.time())[:-8],
            ciName=course.tocCName,ciType=course.tocType,ciD=TeacherInfo.objects.get(tNo=course.tocTeacher_id).tD,
            ciDM=TeacherInfo.objects.get(tNo=course.tocTeacher_id).tDM,ciScore=course.tocScore,ciCapacity=course.tocCapacity,ciTerm=course.tocTerm
        )
        obj.save()
        Course(
            cNo=obj, cName=obj.ciName, cDepart=obj.ciD, cDepartMajor=obj.ciDM,
            cTerm=obj.ciTerm, cCapacity=obj.ciCapacity, cType=obj.ciType,
            cScore=obj.ciScore, cTeacher=TeacherInfo.objects.get(tNo=course.tocTeacher_id)
        ).save()
    return redirect('/release_html/')