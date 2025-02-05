"""
Django settings for dadokdadok project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ SECRET_KEY (배포 시 보안 강화 필요)
SECRET_KEY = 'django-insecure-8pv46p(-rc3hi%-7k21p-^x(k!5s2f6wen-lip92(4ei4o7$f('

# ✅ 개발 환경 설정 (배포 시 DEBUG = False 필요)
DEBUG = True

# ✅ 모든 호스트에서 접근 가능 (배포 시 특정 도메인만 허용)
ALLOWED_HOSTS = ['*']

# ✅ INSTALLED_APPS 설정
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user',
    'book',
    'review',
    'goal',
    'recommendation',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ✅ CORS 설정 (배포 시 특정 도메인만 허용)
CORS_ALLOW_ALL_ORIGINS = True  # 개발 중 모든 요청 허용 (배포 시 변경)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

ROOT_URLCONF = 'dadokdadok.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'dadokdadok.wsgi.application'

# ✅ 데이터베이스 설정 (기본 SQLite 사용)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ✅ 비밀번호 검증 설정
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ✅ 언어 및 시간대 설정
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

# ✅ Static & Media 파일 설정
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ✅ 사용자 모델 설정
AUTH_USER_MODEL = 'user.CustomUser'

# ✅ REST Framework 기본 설정
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # ✅ 기본 권한 변경
    ]
}

# ✅ JWT 설정 (토큰 만료 시간 조절)
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# ✅ 로그인 및 로그아웃 리디렉션 설정
LOGIN_URL = '/user/login/'
LOGOUT_REDIRECT_URL = '/'

# ✅ 네이버 API 설정 (하드코딩된 값 유지)
NAVER_CLIENT_ID = "XuZkPyhdBVtFtXAvM4x9"
NAVER_CLIENT_SECRET = "qc9LqfIhrj"
NAVER_BOOKS_API_URL = "https://openapi.naver.com/v1/search/book.json"

