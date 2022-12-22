from django.urls import path
from student import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordChangeView

urlpatterns = [
path('studentclick', views.studentclick_view),
path('studentlogin', LoginView.as_view(template_name='student/studentlogin.html'),name='studentlogin'),
path('student-dashboard', views.student_dashboard_view,name='student-dashboard'),
path('student-exam', views.student_exam_view,name='student-exam'),
path('take-exam/<int:pk>', views.take_exam_view,name='take-exam'),
path('mcq-exam/<int:pk>', views.mcq_exam_view,name='mcq-exam'),
path('tfq-exam/<int:pk>', views.tfq_exam_view,name='tfq-exam'),
path('gfq-exam/<int:pk>', views.gfq_exam_view,name='gfq-exam'),

path('ot-password-change', views.ot_password_change,name='ot-password-change'),
path('ot-password-changed', views.ot_password_changed, name='ot-password-changed'),
path('update-info/<int:pk>', views.update_student_view, name='update-info'),

path('student-see-announcement', views.student_see_announcements,name='student-see-announcement'),

path('calculate-marks', views.calculate_marks_view,name='calculate-marks'),
path('view-result', views.view_result_view,name='view-result'),
path('check-marks/<int:pk>', views.check_marks_view,name='check-marks'),
path('student-marks', views.student_marks_view,name='student-marks'),
]
