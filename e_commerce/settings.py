"""
Django settings for e_commerce project.
"""

from pathlib import Path
import os 
import dj_database_url # Used to parse the DATABASE_URL from Render environment

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings
# IMPORTANT: Read sensitive variables from the environment for security
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-(nwk9jn(p*c3q&yw57r%er&hwkkpr*87^gz67ne*gca=%y%i4!')
DEBUG = os.environ.get('DEBUG', 'True') == 'True' 
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',') 


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website',
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    'django.contrib.sites', # Add sites framework if using social auth or specific domain logic
]

SITE_ID = 1

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny', # Change this to IsAuthenticated when React is fully integrated
    ],
}


# -------------------------------------------------------------
# STATIC & MEDIA FILE CONFIGURATION
# -------------------------------------------------------------

# Static files (CSS, JavaScript, Images) URL
STATIC_URL = '/static/'

# Location where collectstatic will put files for production
STATIC_ROOT = BASE_DIR / 'staticfiles' 

# Additional directories for static files (where your 'css' folder is)
STATICFILES_DIRS = [
    BASE_DIR / 'website' / 'static', 
]

# Media Files (User Uploaded Content)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media' 


# -------------------------------------------------------------
# CORS AND SECURITY
# -------------------------------------------------------------

CORS_ALLOW_ALL_ORIGINS = False # Set to False for production security
CORS_ALLOWED_ORIGINS = [
    # Add your deployed React domain here
    'https://react-2-qcgd.onrender.com',
    # Add your Django domain here (e.g., if API is on a sub-domain)
    # 'https://e-commerce-qgmj.onrender.com', 
    'http://localhost:3000', # Common local React port
    'http://127.0.0.1:3000',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Force HTTPS and set security headers in production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    
# -------------------------------------------------------------
# URLS AND TEMPLATES
# -------------------------------------------------------------

ROOT_URLCONF = 'e_commerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'e_commerce.wsgi.application'


# -------------------------------------------------------------
# DATABASE CONFIGURATION (Conditional for Local vs. Render)
# -------------------------------------------------------------

if os.environ.get('DATABASE_URL'):
    # Production database (PostgreSQL on Render)
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_check=True,
        )
    }
else:
    # Development database (Local MySQL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'e_commerce',
            'USER': 'root',
            'PASSWORD':'root',
            'HOST':'localhost',
            'PORT':'3306'
        }
    }


# -------------------------------------------------------------
# AUTHENTICATION AND MODEL SETUP
# -------------------------------------------------------------

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


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'website.AuthUser' # Custom user model