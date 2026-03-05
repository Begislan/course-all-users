from django.urls import path

from front import views

urlpatterns = [
    path('', views.home),

    # teacher
    path('courses/', views.teacher_all, name='courses'),
    path('courses/<int:course_id>/', views.teacher_all, name='course_detail'),
    path('courses/<int:course_id>/<int:lesson_id>/', views.teacher_all, name='lesson_detail'),

    # course teacher
    path('edit-course/<int:course_id>/', views.edit_course, name='edit_course'),
    path('delete-course/<int:course_id>/', views.delete_course, name='delete_course'),
    path('courses/add/', views.add_course, name='add_course'),

    # lesson teacher
    path('courses/<int:course_id>/lessons/add/', views.add_lesson, name='add_lesson'),
    path('lessons/<int:lesson_id>/edit/', views.edit_lesson, name='edit_lesson'),
    path('lessons/<int:lesson_id>/delete/', views.delete_lesson, name='delete_lesson'),

    # content
    path('lessons/<int:lesson_id>/content/add/', views.add_content, name='add_content'),
    path('content/<int:content_id>/edit/', views.edit_content, name='edit_content'),
    path('content/<int:content_id>/delete/', views.delete_content, name='delete_content'),

    # student
    path('student/', views.student, name='student'),
    # path('lesson/<int:id>/', views.lesson, name='lesson'),
    path('lessons/<int:course_id>/', views.course_view, name='course_view'),
    path('lessons/<int:course_id>/<int:lesson_id>/', views.course_view, name='course_lesson'),


    #users
    path('users/', views.users, name='users'),
    path('ipload_user/<int:user_id>/', views.upload_users, name='upload_users'),

    #courses
    path('admin_courses/', views.admin_courses, name='admin_courses'),
]
 