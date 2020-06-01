"""db_designer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *
from lh.views import *
from yhn.views import *
from yf.views import *
from hg.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index),

    #lh
    path('login/',login),

    #yhn
    path('add_depart_html/',AddDepartHtml),
    path('add_depart/',AddDepart),
    path('add_depart_major_html/',AddDepartMajorHtml),
    path('add_depart_major/',AddDepartMajor),
    path('add_teacher_html/',AddTeacherHtml),
    path('add_teacher/',AddTeacher),
    path('add_base_course_html/',AddBaseCourseHtml),
    path('add_base_course/',AddBaseCourse),

    path('del_depart/',DelDepart),
    path('del_depart_major/',DelDepartMajor),
    path('del_teacher/',DelTeacher),
    path('del_base_course/',DelBaseCourse),

    #yf
    path('teacher_add_course_html/',TeacherAddCourseHtml),
    path('teacher_add_course/',TeacherAddCourse),
    path('teacher_add_stu_html/',TeacherAddStuHtml),
    path('teacher_add_stu/',TeacherAddStu),
    path('teacher_choose_course/',TeacherChooseCourse),
    path('teacher_edit_grade_html/',TeacherEditGradeHtml),
    path('teacher_edit_grade/',TeacherEditGrade),

    #hg
    path('stu_add_course_html/',StuAddCourseHtml),
    path('stu_add_course/',StuAddCourse),
    path('stu_del_course/',StuDelCourse),

    #lh
    path('release_html/',ReleaseHtml),
    path('release/<int:id>/',Release),
]
