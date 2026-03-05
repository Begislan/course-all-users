from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime

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

# Коддорду убактылуу сактоочу модель
class EmailOTP(models.Model):
    email = models.EmailField()
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # Код 5 мүнөткө гана жарактуу
        return self.created_at >= timezone.now() - datetime.timedelta(minutes=5)