from django.urls import path,include,re_path
from django.contrib import admin
from exam import views
from django.contrib.auth.views import LogoutView,LoginView
from django.urls import path


urlpatterns = [
   
    path('admin/', admin.site.urls),
    path('teacher/',include('teacher.urls')),
    path('student/',include('student.urls')),
    


    path('',views.home_view,name=''),
    path('logout', LogoutView.as_view(template_name='exam/index.html'),name='logout'),
    path('contact_admin', views.contact_admin_view, name='contact_admin'),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),



    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='exam/adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('admin-teacher', views.admin_teacher_view,name='admin-teacher'),
    path('admin-teachersignup', views.admin_teacher_signup_view, name='admin-teachersignup'),
    path('admin-view-teacher', views.admin_view_teacher_view,name='admin-view-teacher'),
    path('admin-edit-teacher', views.admin_edit_teacher_view,name='admin-edit-teacher'),
    path('update-teacher/<int:pk>', views.update_teacher_view,name='update-teacher'),
    path('delete-teacher/<int:pk>', views.delete_teacher_view,name='delete-teacher'),
    path('reset-teacher-password/<int:pk>', views.reset_teacher_password_view,name='reset-teacher-password'),

    path('admin-student', views.admin_student_view,name='admin-student'),
    path('admin-studentsignup', views.admin_student_signup_view, name='admin-studentsignup'),
    path('admin-view-student', views.admin_view_student_view,name='admin-view-student'),
    path('admin-edit-student', views.admin_edit_student_view,name='admin-edit-student'),
    path('update-student/<int:pk>', views.update_student_view,name='update-student'),
    path('delete-student/<int:pk>', views.delete_student_view,name='delete-student'),
    path('reset-student-password/<int:pk>', views.reset_student_password_view,name='reset-student-password'),
    path('admin-add-announcement', views.admin_add_announcement,name='admin-add-announcement'),
    path('admin-see-announcement', views.admin_see_announcements,name='admin-see-announcement'),


    path('admin-view-exam', views.admin_view_exam_view,name='admin-view-exam'),
    path('delete-exam/<int:pk>', views.delete_exam_view,name='delete-exam'),
    path('admin-edit-exam', views.admin_edit_exam_view,name='admin-edit-exam'),

  
    path('view-question/<int:pk>', views.view_question_view,name='view-question'),
    path('delete-question/<int:pk>', views.delete_question_view,name='delete-question'),

]
