import os
from pathlib import Path

# Сиздин проекттин папкасы
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-@xyftd6ws0bd=*4^(-f4lzpz*sr0+$zvx36jns-%kd1&iaud7('

DEBUG = True

ALLOWED_HOSTS = ['*']

# Колдонмолордун тизмеси
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'front',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Шаблондор үчүн базалык папка
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# База - SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Пароль текшерүүчүлөр (Окуу процессинде жеңилдик үчүн өчүрүлдү)
AUTH_PASSWORD_VALIDATORS = []

# Тил жана Убакыт (Бишкек убактысы)
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Asia/Bishkek'
USE_I18N = True
USE_TZ = True

# Статикалык жана Медиа файлдар
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Колдонуучунун Модели ---
AUTH_USER_MODEL = 'accounts.CustomUser'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'login'

# --- Сессиялар (Сеанстар) ---
SESSION_COOKIE_AGE = 7200  # 2 саат
SESSION_SAVE_EVERY_REQUEST = True

# --- Чоң файлдарды жүктөө (10MB чейин) ---
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760

# --- EMAIL SMTP ТУУРАЛОО (Код жөнөтүү үчүн) ---
# КӨҢҮЛ БУРУҢУЗ: Google почтаңыздан "App Password" алууңуз керек
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'ishakishakov00@gmail.com' # Почтаңызды жазыңыз
EMAIL_HOST_PASSWORD = 'nboz ttih qcak rsip' # 16 тамгалуу App Password жазыңыз
DEFAULT_FROM_EMAIL = f'Bilim Platform <{EMAIL_HOST_USER}>'