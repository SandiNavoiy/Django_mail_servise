import os
from pathlib import Path
from dotenv import load_dotenv
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# для загрузки секретных данных в переменные среды, обращение к файлу .env
dot_env = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=dot_env)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-c)(xp%=jwbaczje&0q^kjwv7%3j4z%$dq)nm5#4bqab0x@p5td'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') == 'True'

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'users',
    'crispy_forms',
    'crispy_bootstrap4',
    'mailing',
    'client'
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
        'DIRS': [],
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

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Подключение БД
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DATABASES_NAME'),  # Название БД
        'USER': os.getenv('DATABASES_USER'),  # Пользователь для подключения
        'PASSWORD': os.getenv('DATABASES_PASSWORD'),  # Пароль для этого пользователя
        'HOST': '127.0.0.1',  # Адрес, на котором развернут сервер БД
        'PORT': 5432,  # Порт, на котором работает сервер БД
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
# выбор языка
LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = (BASE_DIR / 'static',)

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# базовые урлы для медиа данных
MEDIA_URL = '/media/'  # набор полей которые отвечают за сохранение файлов вне модели
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# переопределение модели пользователя
AUTH_USER_MODEL = 'users.User'
# подключение кристи формс
CRISPY_TEMPLATE_PACK = "bootstrap4"

LOGIN_REDIRECT_URL = '/'  # редирект для автоаризации
LOGOUT_REDIRECT_URL = '/'  # редирект для выхода из автоаризации

# настройки почты
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER')

EMAIL_HOST = 'smtp.yandex.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True


#кеширование
CACHE_ENABLED = True
if CACHE_ENABLED:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": os.getenv('CACHES_LOCATION'),
            "TIMEOUT": 300 # Ручная регулировка времени жизни кеша в секундах, по умолчанию 300
        }
    }