from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from exam import models as QMODEL
from student import models as SMODEL
from exam import forms as QFORM
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from  .decorators import allowed_users
from django.contrib.auth.decorators import permission_required

#for showing signup/login button for teacher
def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'teacher/teacherclick.html')

def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

@allowed_users(allowed_roles=['TEACHER'])
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    dict={
    
    'total_exam':QMODEL.Exam.objects.all().count(),
    'total_question':QMODEL.multichoice_question.objects.all().count(),
    'total_student':SMODEL.Student.objects.all().count()
    }
    return render(request,'teacher/teacher_dashboard.html',context=dict)

@allowed_users(allowed_roles=['TEACHER'])
@user_passes_test(is_teacher)
def teacher_exam_view(request):
    return render(request,'teacher/teacher_exam.html')


@allowed_users(allowed_roles=['TEACHER'])
@user_passes_test(is_teacher)
def teacher_add_exam_view(request):
    examForm=QFORM.ExamForm()
    if request.method=='POST':
        examForm=QFORM.ExamForm(request.POST)
        exam = examForm.save(commit=False)
        teacher = models.Teacher.objects.all().filter(user=request.user.id)[:1].get()
        subject_id=QMODEL.Subject.objects.get(id=request.POST.get('subjectID'))
        class_id=QMODEL.Class.objects.get(id=request.POST.get('classID'))
        if examForm.is_valid():
            exam.subject = subject_id
            exam.class_id = class_id
            exam.teacher = teacher        
            exam.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-view-exam')
    return render(request,'teacher/teacher_add_exam.html',{'examForm':examForm})

@allowed_users(allowed_roles=['TEACHER'])
@user_passes_test(is_teacher)
def teacher_view_exam_view(request):
    teachers=models.Teacher.objects.all().filter(user=request.user.id)[:1].get()
    exams = QMODEL.Exam.objects.all().filter(visiable=True, teacher=teachers)
    return render(request,'teacher/teacher_view_exam.html',{'exams':exams})

@allowed_users(allowed_roles=['TEACHER'])
@user_passes_test(is_teacher)
def delete_exam_view(request,pk):
    exam=QMODEL.Exam.objects.get(id=pk)
    exam.delete()
    return HttpResponseRedirect('/teacher/teacher-view-exam')

# @login_required(login_url='adminlogin')
# def teacher_question_view(request):
#     return render(request,'teacher/teacher_question.html')

@allowed_users(allowed_roles=['TEACHER'])
@user_passes_test(is_teacher)
def teacher_add_question_view(request):
    questionForm=QFORM.QuestionForm()
    if request.method=='POST':
        questionForm=QFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            exam=QMODEL.Exam.objects.get(id=request.POST.get('examID'))
            question.exam=exam
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-view-question')
    return render(request,'teacher/teacher_add_question.html',{'questionForm':questionForm})

@allowed_users(allowed_roles=['TEACHER'])
@user_passes_test(is_teacher)
def teacher_view_question_view(request):
    exams= QMODEL.Exam.objects.all()
    return render(request,'teacher/teacher_view_question.html',{'exams':exams})

@allowed_users(allowed_roles=['TEACHER'])
@user_passes_test(is_teacher)
def see_question_view(request,pk):
    mcq=QMODEL.multichoice_question.objects.all().filter(exam_id=pk)
    tfq=QMODEL.True_false_question.objects.all().filter(exam_id=pk)
    gfq=QMODEL.filling_gap_question.objects.all().filter(exam_id=pk)

    return render(request,'teacher/see_question.html',{'mcq':mcq, 'tfq':tfq, 'gfq':gfq})

@allowed_users(allowed_roles=['TEACHER'])
@user_passes_test(is_teacher)
def remove_mcq_question_view(request,pk):
    question=QMODEL.multichoice_question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/teacher/teacher-view-exam')
    

@allowed_users(allowed_roles=['TEACHER'])
@user_passes_test(is_teacher)
def remove_tfq_question_view(request,pk):
    question=QMODEL.True_false_question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/teacher/teacher-view-exam')

@allowed_users(allowed_roles=['TEACHER'])
@user_passes_test(is_teacher)
def remove_gfq_question_view(request,pk):
    question=QMODEL.filling_gap_question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/teacher/teacher-view-exam')



# first time login password change
@allowed_users(allowed_roles=['TEACHER'])
def ot_password_change(request):
    teacher=models.Teacher.objects.all().filter(user=request.user.id)[:1].get()
    user=models.User.objects.get(id=teacher.user_id)
    new_password = forms.OTPasswordChange()
    if request.method=='POST':
        new_password = forms.OTPasswordChange(request.POST)
        if new_password.is_valid():
            password=request.POST.get('password')
            user.set_password(password)
            user.save()
            teacher.status=True
            teacher.save()
            return HttpResponseRedirect('/teacher/ot-password-changed')
    return render(request,'teacher/teacher_ot_change_password.html',{'new_password':new_password})

def ot_password_changed(request):
    return render(request, 'teacher/password_change_succeseded.html')



# MultiChoice Questions View
@allowed_users(allowed_roles=['TEACHER'])
def teacher_add_MC_question_view(request):
    questionFormMC=QFORM.QuestionForm_multichoice()
    if request.method=='POST':
        questionFormMC=QFORM.QuestionForm_multichoice(request.POST)
        if questionFormMC.is_valid():
            question=questionFormMC.save(commit=False)
            exam=QMODEL.Exam.objects.get(id=request.POST.get('examID'))
            question.exam=exam
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-add-MC-question')
    return render(request,'teacher/teacher_add_MC_question.html',{'questionFormMC':questionFormMC})

#this view is true/false questions
@allowed_users(allowed_roles=['TEACHER'])
def teacher_add_TF_question_view(request):
    questionFormTF=QFORM.Truefalse()
    if request.method=='POST':
        questionFormTF=QFORM.Truefalse(request.POST)
        if questionFormTF.is_valid():
            question=questionFormTF.save(commit=False)
            exam=QMODEL.Exam.objects.get(id=request.POST.get('examID'))
            question.exam=exam
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-add-TF-question')
    return render(request,'teacher/teacher_add_TF_question.html',{'questionFormTF':questionFormTF})

#this view is Gapfilling questions
@allowed_users(allowed_roles=['TEACHER'])
def teacher_add_gapfilling_view(request):
    questionFormGapF=QFORM.Gapfilling()
    if request.method=='POST':
        questionFormGapF=QFORM.Gapfilling(request.POST)
        if questionFormGapF.is_valid():
            question=questionFormGapF.save(commit=False)
            exam=QMODEL.Exam.objects.get(id=request.POST.get('examID'))
            question.exam=exam
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-add-GF-question')
    return render(request,'teacher/teacher_add_gapfilling_questions.html',{'questionFormGapF':questionFormGapF})    


def teachers_in_same_dep(request):
    cur_teacher=models.Teacher.objects.filter(user=request.user.id)[:1].get()
    teachers=models.Teacher.objects.all().filter(subject=cur_teacher.subject).exclude(user=request.user) 
    return render(request,'teacher/teachers_in_same_dep.html',{'teachers':teachers})


# this is for hidden exams
@allowed_users(allowed_roles=['TEACHER'])
@user_passes_test(is_teacher)
def teacher_view_hidden_exam_view(request):
    teachers=models.Teacher.objects.all().filter(user=request.user.id)[:1].get()
    exams = QMODEL.Exam.objects.all().filter(visiable=False, teacher=teachers)
    return render(request,'teacher/hidden_exams.html',{'exams':exams})


@allowed_users(allowed_roles=['TEACHER'])
@user_passes_test(is_teacher)
def make_exam_visiable(request, pk):
    exam = QMODEL.Exam.objects.get(id=pk)
    exam.visiable=True
    exam.save()
    return HttpResponseRedirect('/teacher/teacher-view-hidden-exam')


@allowed_users(allowed_roles=['TEACHER'])
@user_passes_test(is_teacher)
def make_exam_invisiable(request, pk):
    exam = QMODEL.Exam.objects.get(id=pk)
    exam.visiable=False
    exam.save()
    return HttpResponseRedirect('/teacher/teacher-view-exam')


# Announcements
@allowed_users(allowed_roles=['TEACHER'])
def teacher_add_announcement(request):
    announcement_form = QFORM.Announcement()
    if request.method=='POST':
        announcement_form = QFORM.Announcement(request.POST)
        if announcement_form.is_valid():
            announcement = announcement_form.save(commit=False)
            announcement.author_id = request.user.id
            announcement.save()
        return HttpResponseRedirect('teacher-see-announcement')
    return render(request,'teacher/create_announcement.html', {'announcement_form':announcement_form})


@allowed_users(allowed_roles=['TEACHER'])
def teacher_see_announcements(request):
    announcements = reversed(QMODEL.Announcement.objects.all())
    return render(request,'teacher/view_announcements.html',{'announcements':announcements})

