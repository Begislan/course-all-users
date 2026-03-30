from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime

# 1. Колдонуучу модели
class CustomUser(AbstractUser):
    TYPE_USER = [
        ('teacher', 'Преподаватель'),
        ('student', 'Студент'),
        ('inactive', 'Неактивный'),
    ]

    photo = models.ImageField(upload_to='user_photos/', verbose_name='Фото пользователя', blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(verbose_name='Телефон номер', max_length=255, blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=TYPE_USER, default='inactive', verbose_name='Тип пользователя')

    def __str__(self):
        return self.username

# 2. Почта аркылуу кирүү (OTP) модели
class EmailOTP(models.Model):
    email = models.EmailField()
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # Код 5 мүнөткө гана жарактуу
        return self.created_at >= timezone.now() - datetime.timedelta(minutes=5)

    def __str__(self):
        return f"OTP for {self.email}"

# 3. Байланышуу билдирүүлөрү үчүн модель
# БУЛ ЖЕРДЕ: Индентацияны оңдодук (EmailOTPнин ичинен чыгардык)
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
        