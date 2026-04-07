import os
import socket
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-t&&__nm8x_jsl8!ck9@+-1e!)_i#+5vn)-lx%p(mch$@fww4py'

DEBUG = True

ALLOWED_HOSTS = ['eizo000.pythonanywhere.com', '127.0.0.1', 'localhost']

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    'tasks.apps.TasksConfig',
    'widget_tweaks',
    'pwa',
    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
]

try:
    HOSTNAME = socket.gethostname()
    if "pythonanywhere" in HOSTNAME or os.path.exists('/var/www/'):
        SITE_ID = 2
    else:
        SITE_ID = 1
except:
    SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
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

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = 'task_list'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Updated Allauth Settings to resolve Deprecation Warnings
ACCOUNT_LOGIN_METHODS = {'username', 'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'none' 
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_FORMS = {'login': 'allauth.account.forms.LoginForm'}

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': [
            'user',
            'repo',
            'read:org',
        ],
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

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
    ],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "tasks.Task": "fas fa-tasks",
        "tasks.Category": "fas fa-layer-group",
        "tasks.Priority": "fas fa-flag",
    },
    "show_ui_builder": False, 
}

JAZZMIN_UI_TWEAKS = {
    "theme": "pulse",                 
    "dark_mode_theme": "darkly",      
    "navbar_fixed": True,
    "sidebar_fixed": True,
}
PWA_APP_NAME = 'Hangarin'
PWA_APP_DESCRIPTION = "Visualizing your productivity and task distribution."
PWA_APP_THEME_COLOR = '#6f42c1'  # Using your purple brand color
PWA_APP_BACKGROUND_COLOR = '#FFFFFF'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'portrait'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_DIR = 'ltr'

# Path to your service worker file
PWA_SERVICE_WORKER_PATH = str(BASE_DIR / 'static' / 'js' / 'serviceworker.js')

# Define your icons (ensure these exist in your static/img folder)
PWA_APP_ICONS = [
    {'src': '/static/img/icon-192.png', 'sizes': '192x192'},
    {'src': '/static/img/icon-512.png', 'sizes': '512x512'}
]