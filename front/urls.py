from django.urls import path
from front import views

urlpatterns = [
    # Негизги барак
    path('', views.home, name='home'),

    # --- МУГАЛИМДИН ПАНЕЛИ (Курстар жана сабактар) ---
    path('courses/', views.teacher_all, name='courses'),
    path('courses/<int:course_id>/', views.teacher_all, name='course_detail'),
    path('courses/<int:course_id>/<int:lesson_id>/', views.teacher_all, name='lesson_detail'),
    
    path('courses/add/', views.add_course, name='add_course'),
    path('edit-course/<int:course_id>/', views.edit_course, name='edit_course'),
    path('delete-course/<int:course_id>/', views.delete_course, name='delete_course'),

    path('courses/<int:course_id>/lessons/add/', views.add_lesson, name='add_lesson'),
    path('lessons/<int:lesson_id>/edit/', views.edit_lesson, name='edit_lesson'),
    path('lessons/<int:lesson_id>/delete/', views.delete_lesson, name='delete_lesson'),

    # --- КОНТЕНТ ЖАНА ТЕСТ БАШКАРУУ (Мугалим үчүн) ---
    path('lessons/<int:lesson_id>/content/add/', views.add_content, name='add_content'),
    path('content/<int:content_id>/edit/', views.edit_content, name='edit_content'),
    path('content/<int:content_id>/delete/', views.delete_content, name='delete_content'),
    path('quiz/<int:quiz_id>/add-question/', views.add_question, name='add_question'),
    
    # Сиздин катаны оңдоочу сап:
    path('lesson/<int:lesson_id>/add_quiz/', views.add_quiz, name='add_quiz'),

    # --- СТУДЕНТТИН БАРАКЧАЛАРЫ ---
    path('student/', views.student, name='student'),
    # Сабакты көрүү (Бир эле жол жетиштүү)
    path('lessons-view/<int:course_id>/<int:lesson_id>/', views.course_view, name='course_view'),  

    # Тест тапшыруу (Студент үчүн)
    path('quiz/<int:lesson_id>/', views.take_quiz, name='take_quiz'),

    # --- АДМИН ЖАНА КОЛДОНУУЧУЛАР ---
    path('users/', views.users, name='users'),
    path('upload_user/<int:user_id>/', views.upload_users, name='upload_users'),
    path('admin_courses/', views.admin_courses, name='admin_courses'),
]