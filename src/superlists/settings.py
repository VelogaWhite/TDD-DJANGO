from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-yn6!va0-@jjwu)5($7u@w5po_#1_dm_yvoa2g(142(vau5+7jx'

# กำหนดค่าเริ่มต้น
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'yp-sawatdee.servequake.com', 'sdp2-2025-group1-django-tdd-app.hf.space']
db_path = BASE_DIR / "db.sqlite3"

# ตรวจสอบว่าเป็นการรันบน Production (Hugging Face หรือ Azure)
if "DJANGO_DEBUG_FALSE" in os.environ:
    DEBUG = False
    SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", SECRET_KEY)
    
    if "DJANGO_ALLOWED_HOST" in os.environ:
        ALLOWED_HOSTS.append(os.environ["DJANGO_ALLOWED_HOST"])
        
    db_path = os.environ.get("DJANGO_DB_PATH", BASE_DIR / "db.sqlite3")

    # --- การตั้งค่าความปลอดภัย (สำคัญมากสำหรับ CSRF) ---
    
    # 1. ตรวจสอบว่าเป็น HTTPS (Hugging Face) หรือ HTTP (Azure/Dev)
    # ถ้าโดเมนไม่มี sdp2-2025... (Hugging Face) แสดงว่าเป็น Azure HTTP
    if 'hf.space' in os.environ.get("DJANGO_ALLOWED_HOST", "") or 'huggingface.co' in os.environ.get("HTTP_REFERER", ""):
        # สำหรับ Hugging Face (HTTPS)
        SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
        CSRF_COOKIE_SECURE = True
        SESSION_COOKIE_SECURE = True
        CSRF_COOKIE_SAMESITE = 'None'
        SESSION_COOKIE_SAMESITE = 'None'
    else:
        # สำหรับ Azure (HTTP) - ต้องปิด Secure เพื่อให้ส่ง Cookie ผ่าน HTTP ได้
        SECURE_PROXY_SSL_HEADER = None
        CSRF_COOKIE_SECURE = False
        SESSION_COOKIE_SECURE = False
        CSRF_COOKIE_SAMESITE = 'Lax'
        SESSION_COOKIE_SAMESITE = 'Lax'
else:
    # สำหรับ Development (Local)
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False

# ยืนยัน Trusted Origins ให้ครบทั้งสองโปรโตคอล
CSRF_TRUSTED_ORIGINS = [
    'https://sdp2-2025-group1-django-tdd-app.hf.space',
    'http://yp-sawatdee.servequake.com',
    'https://yp-sawatdee.servequake.com'
]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "lists",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'superlists.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'superlists.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": db_path  
    }
}

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "static"
X_FRAME_OPTIONS = 'ALLOWALL'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {"root": {"handlers": ["console"], "level": "INFO"}},
}