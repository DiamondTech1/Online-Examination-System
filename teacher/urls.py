from django.urls import path
from teacher import views
from django.contrib.auth.views import LoginView

urlpatterns = [
path('teacherclick', views.teacherclick_view),
path('teacherlogin', LoginView.as_view(template_name='teacher/teacherlogin.html'),name='teacherlogin'),
path('teacher-dashboard', views.teacher_dashboard_view,name='teacher-dashboard'),
path('teacher-exam', views.teacher_exam_view,name='teacher-exam'),
path('teacher-add-exam', views.teacher_add_exam_view,name='teacher-add-exam'),
path('teacher-view-exam', views.teacher_view_exam_view,name='teacher-view-exam'),
path('delete-exam/<int:pk>', views.delete_exam_view,name='delete-exam'),
path('teachers-in-same-dep', views.teachers_in_same_dep,name='teachers-in-same-dep'),
path('teacher-view-hidden-exam', views.teacher_view_hidden_exam_view,name='teacher-view-hidden-exam'),
path('make-exam-visiable/<int:pk>', views.make_exam_visiable, name='make-exam-visiable'),
path('make-exam-invisiable/<int:pk>', views.make_exam_invisiable, name='make-exam-invisiable'),

path('ot-password-change', views.ot_password_change,name='ot-password-change'),
path('ot-password-changed', views.ot_password_changed, name='ot-password-changed'),

path('teacher-add-announcement', views.teacher_add_announcement,name='teacher-add-announcement'),
path('teacher-see-announcement', views.teacher_see_announcements,name='teacher-see-announcement'),

# path('teacher-question', views.teacher_question_view,name='teacher-question'),
path('teacher-add-question', views.teacher_add_question_view,name='teacher-add-question'),
path('teacher-view-question', views.teacher_view_question_view,name='teacher-view-question'),
path('see-question/<int:pk>', views.see_question_view,name='see-question'),
path('remove-mcq-question/<int:pk>', views.remove_mcq_question_view,name='remove-mcq-question'),
path('remove-tfq-question/<int:pk>', views.remove_tfq_question_view,name='remove-tfq-question'),
path('remove-gfq-question/<int:pk>', views.remove_gfq_question_view,name='remove-gfq-question'),

path('teacher-add-MC-question', views.teacher_add_MC_question_view,name='teacher-add-MC-question'),
path('teacher-add-TF-question', views.teacher_add_TF_question_view,name='teacher-add-TF-question'),
path('teacher-add-GF-question', views.teacher_add_gapfilling_view,name='teacher-add-GF-question'),
]
