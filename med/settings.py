import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+9*v^ww%sea&$#45uyuldikymgcijrq6&vp@y8s97%&3@vzvli'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'bootstrap3',
    'users',
    'med',
    'media',
    'search',
    'reversion',
    'logs'
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

ROOT_URLCONF = 'med.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',  # From re2o
                'med.context_processors.context_user',  # From re2o
            ],
        },
    },
]

WSGI_APPLICATION = 'med.wsgi.application'


# Django crispy forms

CRISPY_TEMPLATE_PACK = 'bootstrap4'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


# Emails

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_SSL = False
# EMAIL_HOST = ''
# EMAIL_PORT = 25
# EMAIL_HOST_USER = 'change_me'
# EMAIL_HOST_PASSWORD = 'change_me'

DEFAULT_FROM_EMAIL = 'webmaster@localhost'
SERVER_EMAIL = 'root@localhost'

# Set these to True if using HTTPS
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# Send 500 errors to these emails
# eg: ADMINS = [('pseudo', 'mymail@something.org')]
ADMINS = []






### Under this comment it is code from re2o

# Auth definition

PASSWORD_HASHERS = (
    'med.login.SSHAPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
)

AUTH_USER_MODEL = 'users.User'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# django-bootstrap3 config dictionnary
BOOTSTRAP3 = {
            'jquery_url': '/static/js/jquery-2.2.4.min.js',
            'base_url': '/static/bootstrap/',
            'include_jquery': True,
        }
BOOTSTRAP_BASE_URL = '/static/bootstrap/'

PAGINATION_NUMBER = 25
PAGINATION_LARGE_NUMBER = 8

# Security settings
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_AGE = 60 * 60 * 3

# Association information

SITE_NAME = "Re2o.rez"

# Main extension used in asso
MAIN_EXTENSION = ".rez"

LOGO_PATH = "static_files/logo.png"

# Number of hours a token remains valid after having been created.  Numeric and string
# versions should have the same meaning.
REQ_EXPIRE_HRS = 48
REQ_EXPIRE_STR = '48 heures'

# Affchage des résultats
SEARCH_RESULT = 15

# Décision radius à prendre
RADIUS_VLAN_DECISION = {
    'VLAN_NOK' : 42,
    'VLAN_OK' : 69,
}

MAX_EMPRUNT = 5

AUTHORIZED_IP_RANGE = '0.0.0.0/0'
AUTHORIZED_IP6_RANGE = '*'
SEARCH_DISPLAY_PAGE = 10
