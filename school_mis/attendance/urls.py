from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.mark_attendance, name='mark_attendance'),
    path('records/', views.attendance_list, name='attendance_list'),
    path('students/add/', views.add_student, name='add_student'),
]
 
