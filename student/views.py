from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from exam import models as QMODEL
from teacher import models as TMODEL
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from  .decorators import allowed_users
from django.contrib.auth.decorators import permission_required


#for showing signup/login button for student
def studentclick_view(request):
    error = "Username or password is incorrect!"
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    else:
        return render(request,'student/studentlogin.html', {'error': error})
    return render(request,'student/studentclick.html')



def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

@allowed_users(allowed_roles=['STUDENT'])
@user_passes_test(is_student)
def student_dashboard_view(request):
    std=models.Student.objects.all().filter(user=request.user.id)[:1].get()
    exams=QMODEL.Exam.objects.all().filter(class_id=std.class_id, visiable=True).count()
    dict={
    
    'total_exam':exams,
    'total_question':QMODEL.multichoice_question.objects.all().count(),
    }
    return render(request,'student/student_dashboard.html',context=dict)

@allowed_users(allowed_roles=['STUDENT'])
@user_passes_test(is_student)
def student_exam_view(request):
    std=models.Student.objects.all().filter(user=request.user.id)[:1].get()
    exams=QMODEL.Exam.objects.all().filter(class_id=std.class_id, visiable=True)
    return render(request,'student/student_exam.html',{'exams':exams})

@allowed_users(allowed_roles=['STUDENT'])
@user_passes_test(is_student)
def take_exam_view(request,pk):
    exam=QMODEL.Exam.objects.get(id=pk)
    total_mcq=QMODEL.multichoice_question.objects.all().filter(exam=exam).count()
    total_tfq=QMODEL.True_false_question.objects.all().filter(exam=exam).count()
    total_gfq=QMODEL.filling_gap_question.objects.all().filter(exam=exam).count()
    total_questions = total_mcq+total_tfq+total_gfq
    exam_time = exam.timmer
    mcq=QMODEL.multichoice_question.objects.all().filter(exam=exam)
    tfq=QMODEL.True_false_question.objects.all().filter(exam=exam)
    gfq=QMODEL.filling_gap_question.objects.all().filter(exam=exam)
    total_marks=0
    for m in mcq:
        total_marks=total_marks + m.marks
    for t in tfq:
        total_marks=total_marks + t.marks
    for g in gfq:
        total_marks=total_marks + g.marks

    return render(request,'student/take_exam.html',{'exam':exam,'time': exam_time,'total_questions':total_questions,'total_marks':total_marks})


# Questions in exam

@allowed_users(allowed_roles=['STUDENT'])
@user_passes_test(is_student)
def mcq_exam_view(request,pk):
    exam=QMODEL.Exam.objects.get(id=pk)
    mcquestions=QMODEL.multichoice_question.objects.all().filter(exam=exam)

    paginator = Paginator(mcquestions,1)
    try: 
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    
    try:
        mcq=paginator.page(page)
    except(EmptyPage,InvalidPage):
        mcq=paginator.page(paginator.num_pages)

    response= render(request,'student/mcq_exam.html',{'exam':exam,'mcq':mcq})
    response.set_cookie('exam_id',exam.id)
    response.set_cookie('timer',exam.timmer*60)
    return response


@allowed_users(allowed_roles=['STUDENT'])
@user_passes_test(is_student)
def tfq_exam_view(request,pk):
    exam=QMODEL.Exam.objects.get(id=pk)
    tfquestions=QMODEL.True_false_question.objects.all().filter(exam=exam)

    paginator = Paginator(tfquestions,1)
    try: 
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    
    try:
        tfq=paginator.page(page)
    except(EmptyPage,InvalidPage):
        tfq=paginator.page(paginator.num_pages)

    response= render(request,'student/tfq_exam.html',{'exam':exam,'tfq':tfq})
    response.set_cookie('exam_id',exam.id)
    return response


@allowed_users(allowed_roles=['STUDENT'])
@user_passes_test(is_student)
def gfq_exam_view(request,pk):
    exam=QMODEL.Exam.objects.get(id=pk)
    gfquestions=QMODEL.filling_gap_question.objects.all().filter(exam=exam)

    paginator = Paginator(gfquestions,1)
    try: 
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    
    try:
        gfq=paginator.page(page)
    except(EmptyPage,InvalidPage):
        gfq=paginator.page(paginator.num_pages)

    response= render(request,'student/gfq_exam.html',{'exam':exam,'gfq':gfq})
    response.set_cookie('exam_id',exam.id)
    return response


@allowed_users(allowed_roles=['STUDENT'])
@user_passes_test(is_student)
def calculate_marks_view(request):
    response = HttpResponseRedirect('view-result')
    if request.COOKIES.get('exam_id') is not None:
        exam_id = request.COOKIES.get('exam_id')
        exam=QMODEL.Exam.objects.get(id=exam_id)
        
        total_marks=0
        questions=QMODEL.multichoice_question.objects.all().filter(exam=exam)
        for i in range(len(questions)):
            
            selected_ans = request.COOKIES.get(str(i+1))
            print(selected_ans)
            actual_answer = questions[i].answer
            print(actual_answer)
            response.delete_cookie(str(i+1))

            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks

        questions=QMODEL.True_false_question.objects.all().filter(exam=exam)
        for i in range(len(questions)):
            
            selected_ans = request.COOKIES.get(str(i+101))
            print(selected_ans)
            actual_answer = questions[i].answer
            print(actual_answer)
            response.delete_cookie(str(i+101))
            
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks

        questions=QMODEL.filling_gap_question.objects.all().filter(exam=exam)
        for i in range(len(questions)):
            
            selected_ans = request.COOKIES.get(str(i+201))
            print(selected_ans)
            actual_answer = questions[i].answer
            print(actual_answer)
            response.delete_cookie(str(i+201))
            
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        student = models.Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks=total_marks
        result.exam=exam
        result.student=student
        result.save()


        return response


@allowed_users(allowed_roles=['STUDENT'])
@user_passes_test(is_student)
def view_result_view(request):
    exams=QMODEL.Exam.objects.all()
    return render(request,'student/view_result.html',{'exams':exams})
    

@allowed_users(allowed_roles=['STUDENT'])
@user_passes_test(is_student)
def check_marks_view(request,pk):
    exam=QMODEL.Exam.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.all().filter(exam=exam).filter(student=student)
    return render(request,'student/check_marks.html',{'results':results})

@allowed_users(allowed_roles=['STUDENT'])
@user_passes_test(is_student)
def student_marks_view(request):
    exams=QMODEL.Exam.objects.all()
    return render(request,'student/student_marks.html',{'exams':exams})
  

@allowed_users(allowed_roles=['STUDENT'])
def ot_password_change(request):
    student=models.Student.objects.all().filter(user=request.user.id)[:1].get()
    user=models.User.objects.get(id=student.user_id)
    new_password = forms.OTPasswordChange()
    if request.method=='POST':
        new_password = forms.OTPasswordChange(request.POST)
        if new_password.is_valid():
            password=request.POST.get('password')
            user.set_password(password)
            user.save()
            student.status=True
            student.save()
            return HttpResponseRedirect('/student/ot-password-changed')
    return render(request,'student/student_ot_change_password.html',{'new_password':new_password})

def ot_password_changed(request):
    return render(request, 'student/password_change_succeseded.html')


@allowed_users(allowed_roles=['STUDENT'])
def update_student_view(request,pk):
    student=models.Student.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    userForm=forms.StudentUserForm(instance=user)
    studentForm=forms.StudentForm(request.FILES,instance=student)
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST,instance=user)
        studentForm=forms.StudentForm(request.POST,request.FILES,instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            studentForm.save()
            return HttpResponseRedirect('/student/student-dashboard')
    return render(request,'student/update_student.html',context=mydict)



@allowed_users(allowed_roles=['STUDENT'])
def student_see_announcements(request):
    announcements = reversed(QMODEL.Announcement.objects.all())
    return render(request,'student/view_announcements.html',{'announcements':announcements})