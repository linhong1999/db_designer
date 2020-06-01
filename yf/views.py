from django.shortcuts import render, redirect

from yzk.models import CourseInfoList
from .models import *
from lh.views import operate_log, LoginInfo
from yhn.models import *
from hg.models import *
# Create your views here.
# @operate_log(('添加了','开放课程'))

def TeacherAddCourseHtml(req):
    iden = req.session['lIden']
    no = req.session['lNo']
    #把可选基础课列出来
    course_list = CourseInfo.objects.all()
    #该教师已经 开放的课程
    teacher_course_list = TeacherInfo.objects.get(tNo=no).teacheropencourse_set.all()
    #全校课程
    other_course_list = Course.objects.all()
    return render(req,'teacher_add_course.html',{
        'course_list':course_list,'teacher_course_list':teacher_course_list,
        'other_course_list':other_course_list
    })
@operate_log('开放了','课程')
def TeacherAddCourse(req):
    kwargs = {key:req.POST.get(key) for key in ['tocType','tocCName','tocScore','tocCapacity','tocOpenTime','tocTerm']}
    kwargs['tocStatus'] = '1'
    kwargs['tocTeacher'] = TeacherInfo.objects.get(tNo=req.session['lNo'])
    TeacherOpenCourse.objects.create(**kwargs)
    return redirect('/teacher_add_course_html/')

@operate_log('开放了','课程')
def TeacherChooseCourse(req):
    for item,time,term in zip(req.POST.getlist('ciName'),req.POST.getlist('tocOpenTime'),req.POST.getlist('tocTerm')):
        # Course.objects.filter(cNo_id=item).update(cTeacher=TeacherInfo.objects.get(tNo=req.session['lNo']))
        obj = CourseInfo.objects.get(ciNo=item)
        Course.objects.create(
            cNo=obj,cName=obj.ciName,cDepart=obj.ciD,cDepartMajor=obj.ciDM,
            cTerm=obj.ciTerm,cCapacity=obj.ciCapacity,cType=obj.ciType,
            cScore=obj.ciScore,cTeacher=TeacherInfo.objects.get(tNo=req.session['lNo'])
        )
        TeacherOpenCourse.objects.create(
            tocTeacher=TeacherInfo.objects.get(tNo=req.session['lNo']),
            tocType=obj.ciType,tocCapacity=obj.ciCapacity,tocCName=obj.ciName,
            tocScore=obj.ciScore,tocStatus='1',tocOpenTime=time,
            tocTerm=term
        )
        print(item,time,term)
    return redirect('/teacher_add_course_html/')


def TeacherAddStuHtml(req):
    item = [{
        'sNo':item.sNo,'sName':item.sName,'sSex':item.get_sSex_display(),
        's_mentor':item.s_mentor.tName,'sYear':item.sYear,'scNo':StudentClass.objects.get(scSNo_id=item.sNo).scNo,
        'sD':Depart.objects.get(dNo=item.sD_id).dName,'sDM':DepartMajor.objects.get(dmNo=item.sDM_id).dmName
    } for item in Student.objects.filter(s_mentor_id=req.session['lNo'])]

    return render(req,'teacher_add_stu.html',{'items':item})
@operate_log('添加了','学生')
def TeacherAddStu(req):
    kwargs = {key:req.POST.get(key) for key in ['sNo','sName','sSex','sSex','sYear']}
    #所属院系为添加教师的院系 缺省为
    #就这样吧懒得改
    if req.POST.get('sDM'):
        if DepartMajor.objects.get(dmName=req.POST.get('sDM')):
            kwargs['sDM'] = DepartMajor.objects.get(dmName=req.POST.get('sDM'))
    else:
        kwargs['sDM'] = TeacherInfo.objects.get(tNo=req.session['lNo']).tDM

    if req.POST.get('sD'):
        if Depart.objects.get(dName=req.POST.get('sD')):
            kwargs['sD'] = Depart.objects.get(dName=req.POST.get('sD'))
    else:
        kwargs['sD'] = TeacherInfo.objects.get(tNo=req.session['lNo']).tD

    if req.POST.get('s_mentor'):
        if TeacherInfo.objects.get(tNo=req.POST.get('s_mentor')):
            kwargs['s_mentor'] = TeacherInfo.objects.get(tNo=req.POST.get('s_mentor'))
    else:
        kwargs['s_mentor'] = TeacherInfo.objects.get(tNo=req.session['lNo'])

    stu = Student.objects.create(**kwargs)
    scNo = StudentClass.objects.filter(scDM_id=kwargs['sDM'].dmNo).count()//30 +1
    StudentClass.objects.create(scSNo=stu,scDM=kwargs['sDM'],scD=kwargs['sD'],scNo=kwargs['sYear'] + str(scNo))

    # 当教师添加了一个学生之后
    # 自动补全学生的基础课程
    LoginInfo(lNo=kwargs['sNo'], lIden='0').save()
    for item in CourseInfo.objects.filter(ciType='0'):
        StudentsChoice.objects.create(
            cCNo=Course.objects.get(cNo_id=item.ciNo,cTeacher_id='1000'), cStuNo=stu,cTeacher=TeacherInfo.objects.get(tNo='1002'),
            cGrade='',cStatus='3' , cType='0'
        )#状态为未选 即未选教师 和课程未选一样 选上之后为默认
        CourseInfoList.objects.create(
            cNo=Course.objects.get(cNo_id=item.ciNo,cTeacher_id='1000'),cName=item.ciName,cDepart=item.ciD,cDepartMajor=item.ciDM,
            cTerm=item.ciTerm,cCapacity=item.ciCapacity,cType=item.ciType,cScore=item.ciScore,
            cTeacher=TeacherInfo.objects.get(tNo='1002'),cStudent=Student.objects.get(sNo=kwargs['sNo'])
        )
    # 自动补全学生专业必修课
    for item in Course.objects.filter(cType='0',cDepart=kwargs['sD'],cDepartMajor=kwargs['sDM']):
        StudentsChoice.objects.create(
            cCNo=item, cStuNo=stu, cTeacher=item.cTeacher.all().first(),
            cGrade='', cStatus='3',cType='0'
        )
    return redirect('/teacher_add_stu_html/')



def TeacherEditGradeHtml(req):
    stu_list = CourseInfoList.objects.filter(cTeacher_id=req.session['lNo'])
    return render(req,'teacher_edit_grade.html',{'items':stu_list})

@operate_log('修改了','学生成绩')
def TeacherEditGrade(req):
    if eval(req.POST.get('cGrade'))>=60:
        status = '1'
    else:
        status = '0'
    StudentsChoice.objects.filter(
        cCNo_id=req.POST.get('cCNo'),cStuNo=req.POST.get('sNo'),
        cTeacher_id=req.session['lNo']
    ).update(cGrade=req.POST.get('cGrade'),cStatus=status)
    CourseInfoList.objects.filter(cStudent_id=req.POST.get('sNo'),cNo_id=req.POST.get('cCNo')).\
        update(cGrade=req.POST.get('cGrade'),cStatus=status)
    #更新通过率
    CourseInfoList.objects.filter(cNo_id=req.POST.get('cCNo')).update(
        cPercent=len(CourseInfoList.objects.filter(cNo_id=req.POST.get('cCNo'), cStatus='1')) / len(
            CourseInfoList.objects.filter(cNo_id=req.POST.get('cCNo')))
    )
    return redirect('/teacher_edit_grade_html/')