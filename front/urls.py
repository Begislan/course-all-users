from django.urls import path
from front import views

urlpatterns = [
    # Негизги барактар
    path('', views.home, name='home'),
    path('student/', views.student, name='student'),
    
    # --- МУГАЛИМДИН ПАНЕЛИ ---
    path('courses/', views.teacher_all, name='courses'),
    path('courses/<int:course_id>/', views.teacher_all, name='course_detail'),
    path('courses/<int:course_id>/<int:lesson_id>/', views.teacher_all, name='lesson_detail'),
    
    path('courses/add/', views.add_course, name='add_course'),
    path('edit-course/<int:course_id>/', views.edit_course, name='edit_course'),
    path('delete-course/<int:course_id>/', views.delete_course, name='delete_course'),

    path('courses/<int:course_id>/lessons/add/', views.add_lesson, name='add_lesson'),
    path('lessons/<int:lesson_id>/edit/', views.edit_lesson, name='edit_lesson'),
    path('lessons/<int:lesson_id>/delete/', views.delete_lesson, name='delete_lesson'),

    path('lessons/<int:lesson_id>/content/add/', views.add_content, name='add_content'),
    path('content/<int:content_id>/edit/', views.edit_content, name='edit_content'),
    path('content/<int:content_id>/delete/', views.delete_content, name='delete_content'),
    
    path('lesson/<int:lesson_id>/add_quiz/', views.add_quiz, name='add_quiz'),
    path('quiz/<int:quiz_id>/add-question/', views.add_question, name='add_question'),

    # --- СТУДЕНТТИН БАРАКЧАЛАРЫ ---
    path('lessons-view/<int:course_id>/<int:lesson_id>/', views.course_view, name='course_view'),
    path('lessons-view/<int:course_id>/', views.course_view, name='course_view_start'), 

    path('quiz/<int:lesson_id>/', views.take_quiz, name='take_quiz'),
    
    # 📸 ПРОКТОРИНГ: Скриншот сактоо жолу (ЖАҢЫ)
    path('quiz/save-screenshot/<int:lesson_id>/', views.save_quiz_screenshot, name='save_quiz_screenshot'),

    # --- АДМИН ЖАНА КОЛДОНУУЧУЛАР ---
    path('users/', views.users, name='users'),
    path('upload_user/<int:user_id>/', views.upload_users, name='upload_users'),
    path('admin_courses/', views.admin_courses, name='admin_courses'),
]