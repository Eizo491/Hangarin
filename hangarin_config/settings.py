import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-t&&__nm8x_jsl8!ck9@+-1e!)_i#+5vn)-lx%p(mch$@fww4py'

# Set DEBUG to False when you are ready for final submission
DEBUG = True

# Update with your PythonAnywhere domain
ALLOWED_HOSTS = ['eizo123.pythonanywhere.com', '127.0.0.1']

INSTALLED_APPS = [
    'jazzmin',
    'tasks.apps.TasksConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
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

ROOT_URLCONF = 'hangarin_config.urls'

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

WSGI_APPLICATION = 'hangarin_config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- Standard Auth Configuration ---
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'task_list'
LOGOUT_REDIRECT_URL = 'login'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_TZ = True

# --- Static & Media Files ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Jazzmin Configuration ---
JAZZMIN_SETTINGS = {
    "site_title": "Hangarin Admin",
    "site_header": "Hangarin",
    "site_brand": "Hangarin",
    "welcome_sign": "Welcome to Hangarin Portal",
    "copyright": "Hangarin Ltd",
    "search_model": ["tasks.Task"],
    "show_sidebar": True,
    "navigation_expanded": True,
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "View Dashboard", "url": "task_list", "permissions": ["auth.view_user"]},
        {"model": "tasks.Task"},
    ],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "tasks.Task": "fas fa-tasks",
    },
    "show_ui_builder": False, 
}

JAZZMIN_UI_TWEAKS = {
    "theme": "pulse",                 
    "dark_mode_theme": "darkly",      
    "navbar_fixed": True,
    "sidebar_fixed": True,
}