from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from teacher import models as TMODEL
from student import models as SMODEL
from teacher import forms as TFORM
from student import forms as SFORM
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from  .decorators import allowed_users
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse




def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request,'exam/index.html')


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def afterlogin_view(request):
    if is_student(request.user): 
        account_active=SMODEL.Student.objects.all().filter(user_id=request.user.id,status=True)
        if account_active:
            return redirect('student/student-dashboard')
        else:
            return redirect('student/ot-password-change')
   
                
    elif is_teacher(request.user):
        account_active=TMODEL.Teacher.objects.all().filter(user_id=request.user.id,status=True)
        if account_active:
            return redirect('teacher/teacher-dashboard')
        else:
            return redirect('teacher/ot-password-change')
           
    else:
        return redirect('admin-dashboard')



def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@allowed_users(allowed_roles=['admin'])
def admin_dashboard_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    'total_teacher':TMODEL.Teacher.objects.all().count(),
    'total_exam':models.Exam.objects.all().count(),
    # 'total_question':models.multichoice_question.objects.all().count(),
    }
    teachers= TMODEL.Teacher.objects.all()
    students= SMODEL.Student.objects.all()
    return render(request,'exam/admin_dashboard.html', {'teachers':teachers, 'students':students, 'dict':dict})

@allowed_users(allowed_roles=['admin'])
def admin_teacher_view(request):
    dict={
    'total_teacher':TMODEL.Teacher.objects.all().filter(status=True).count(),
    'pending_teacher':TMODEL.Teacher.objects.all().filter(status=False).count(),
    'salary':TMODEL.Teacher.objects.all().filter(status=True).aggregate(Sum('salary'))['salary__sum'],
    }
    return render(request,'exam/admin_teacher.html',context=dict)

@allowed_users(allowed_roles=['admin'])
def admin_view_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all()
    return render(request,'exam/admin_view_teacher.html',{'teachers':teachers})

@allowed_users(allowed_roles=['admin'])
def admin_edit_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all()
    return render(request,'exam/admin_edit_teacher.html',{'teachers':teachers})

@allowed_users(allowed_roles=['admin'])
def update_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=TMODEL.User.objects.get(id=teacher.user_id)
    userForm=TFORM.TeacherUserForm(instance=user)
    teacherForm=TFORM.TeacherForm(request.FILES,instance=teacher)
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=TFORM.TeacherUserForm(request.POST,instance=user)
        teacherForm=TFORM.TeacherForm(request.POST,request.FILES,instance=teacher)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacherForm.save()
            return redirect('admin-view-teacher')
    return render(request,'exam/update_teacher.html',context=mydict)



@allowed_users(allowed_roles=['admin'])
def delete_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-edit-teacher')



@allowed_users(allowed_roles=['admin'])
def reset_teacher_password_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.set_password('th12345')
    user.save()
    teacher.status=False
    teacher.save()
    return HttpResponseRedirect('/admin-edit-teacher')



#//////////////////////////////////////////////

@allowed_users(allowed_roles=['admin'])
def admin_student_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    }
    return render(request,'exam/admin_student.html',context=dict)

@allowed_users(allowed_roles=['admin'])
def admin_view_student_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'exam/admin_view_student.html',{'students':students})

@allowed_users(allowed_roles=['admin'])
def admin_edit_student_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'exam/admin_edit_student.html',{'students':students})



@allowed_users(allowed_roles=['admin'])
def update_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=SMODEL.User.objects.get(id=student.user_id)
    userForm=SFORM.StudentUserForm(instance=user)
    studentForm=SFORM.StudentForm(request.FILES,instance=student)
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=SFORM.StudentUserForm(request.POST,instance=user)
        studentForm=SFORM.StudentForm(request.POST,request.FILES,instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            studentForm.save()
            return redirect('admin-view-student')
    return render(request,'exam/update_student.html',context=mydict)



@allowed_users(allowed_roles=['admin'])
def delete_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('/admin-edit-student')


@allowed_users(allowed_roles=['admin'])
def reset_student_password_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=User.objects.get(id=student.user_id)
    user.set_password('st12345')
    user.save()
    student.status=False
    student.save()
    return HttpResponseRedirect('/admin-edit-student')


@allowed_users(allowed_roles=['admin'])
def admin_view_exam_view(request):
    exams = models.Exam.objects.all()
    return render(request,'exam/admin_view_exam.html',{'exams':exams})



@allowed_users(allowed_roles=['admin'])
def admin_view_question_view(request):
    exams= models.Exam.objects.all()
    return render(request,'exam/admin_view_question.html',{'exams':exams})

@allowed_users(allowed_roles=['admin'])
def view_question_view(request,pk):
    mcq=models.multichoice_question.objects.all().filter(exam_id=pk)
    tfq=models.True_false_question.objects.all().filter(exam_id=pk)
    gfq=models.filling_gap_question.objects.all().filter(exam_id=pk)

    return render(request,'exam/view_question.html',{'mcq':mcq, 'tfq':tfq, 'gfq':gfq})


@allowed_users(allowed_roles=['admin'])
def delete_question_view(request,pk):
    question=models.multichoice_question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/admin-view-question')

# @allowed_users(allowed_roles=['admin'])
# def admin_view_student_marks_view(request):
#     students= SMODEL.Student.objects.all()
#     return render(request,'exam/admin_view_student_marks.html',{'students':students})

# @allowed_users(allowed_roles=['admin'])
# def admin_view_marks_view(request,pk):
#     exams = models.Exam.objects.all()
#     response =  render(request,'exam/admin_view_marks.html',{'exams':exams})
#     response.set_cookie('student_id',str(pk))
#     return response

# @allowed_users(allowed_roles=['admin'])
# def admin_check_marks_view(request,pk):
#     exam = models.Exam.objects.get(id=pk)
#     student_id = request.COOKIES.get('student_id')
#     student= SMODEL.Student.objects.get(id=student_id)

#     results= models.Result.objects.all().filter(exam=exam).filter(student=student)
#     return render(request,'exam/admin_check_marks.html',{'results':results})
    

def contact_admin_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'exam/contactussuccess.html')
    return render(request, 'exam/contactus.html', {'form':sub})

# Admin adding teacher
@allowed_users(allowed_roles=['admin'])
def admin_teacher_signup_view(request):
    userForm=TFORM.TeacherUserForm()
    teacherForm=TFORM.TeacherForm()
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    mydict1={'userForm':userForm,'teacherForm':teacherForm, 'error': 'Username Already exist'}
    if request.method=='POST':
        userForm=TFORM.TeacherUserForm(request.POST)
        teacherForm=TFORM.TeacherForm(request.POST,request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacher=teacherForm.save(commit=False)
            teacher.user=user
            subject=models.Subject.objects.get(id=request.POST.get('subjectID'))
            teacher.subject = subject
            teacher.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
        # return HttpResponseRedirect('teacherlogin')
    return render(request,'exam/teachersignup.html',context=mydict)


# Student Signup
@allowed_users(allowed_roles=['admin'])
def admin_student_signup_view(request):
    userForm=SFORM.StudentUserForm()
    studentForm=SFORM.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=SFORM.StudentUserForm(request.POST)
        studentForm=SFORM.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            if User.objects.all().filter(username = request.POST.get('username')):
                return render(request,'exam/studentsignup.html',{'userForm':userForm,'studentForm':studentForm, 'error':"Username exists"})
            else:
                user=userForm.save()
                user.set_password(user.password)
                user.save()
                student=studentForm.save(commit=False)
                student.user=user
                class_id=models.Class.objects.get(id=request.POST.get('classID'))
                student.class_id = class_id
                student.save()
                my_student_group = Group.objects.get_or_create(name='STUDENT')
                my_student_group[0].user_set.add(user)
        # return HttpResponseRedirect('studentlogin')
    return render(request,'exam/studentsignup.html',context=mydict)


@allowed_users(allowed_roles=['admin'])
def admin_add_announcement(request):
    announcement_form = forms.Announcement()
    if request.method=='POST':
        announcement_form = forms.Announcement(request.POST)
        if announcement_form.is_valid():
            announcement = announcement_form.save(commit=False)
            announcement.author_id = request.user.id
            announcement.save()
        return HttpResponseRedirect('admin-see-announcement')
    return render(request,'exam/create_announcement.html', {'announcement_form':announcement_form})


@allowed_users(allowed_roles=['admin'])
def admin_see_announcements(request):
    announcements = reversed(models.Announcement.objects.all())
    return render(request,'exam/view_announcements.html',{'announcements':announcements})




@allowed_users(allowed_roles=['admin'])
def admin_edit_exam_view(request):
    exams = models.Exam.objects.all()
    return render(request,'exam/edit_exam.html',{'exams':exams})


@allowed_users(allowed_roles=['admin'])
def delete_exam_view(request,pk):
    exam=models.Exam.objects.get(id=pk)
    exam.delete()
    return HttpResponseRedirect('/admin-edit-exam')