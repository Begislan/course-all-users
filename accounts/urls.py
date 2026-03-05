from django.urls import path
from .views import (
    register_view, 
    login_view,            # Кадимки кирүү функциясы
    forgot_password_view,  # Паролду унутканда Email суроо функциясы
    verify_otp_view,       # Кодду текшерүү функциясы
    logout_view, 
    edit_profile
)

urlpatterns = [
    # Каттоо
    path('register/', register_view, name='signup'),
    
    # Негизги кирүү (Логин жана Пароль менен)
    path('login/', login_view, name='login'),
    
    # Паролду унутуп калганда колдонулуучу жолдор
    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('verify-otp/', verify_otp_view, name='verify_otp'),
    
    # Профиль жана чыгуу
    path('logout/', logout_view, name='logout'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]