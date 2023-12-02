from .import views
from django.urls import path


urlpatterns = [
    path('',views.index,name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('admin_login', views.admin_login, name='admin_login'),

    path('student_home',views.student_home,name='student_home'),
    path('admin_home',views.admin_home,name='admin_home'),
    path('admin_question_view',views.admin_question_view,name='admin_question_view'),
    path('show_answers',views.show_answers,name='show_answers'),
    path('admin_view_answers',views.admin_view_answers,name='admin_view_answers'),
    path('create_question', views.create_question, name='create_question'),
    path('student_view', views.student_view, name='student_view'),
    path('logout', views.logout, name='logout'),
]