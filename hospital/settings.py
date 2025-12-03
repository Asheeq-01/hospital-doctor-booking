from pathlib import Path
import os
import dj_database_url

# ---------------------------------------------------------------------
# BASE DIRECTORY
# ---------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------
# SECURITY
# ---------------------------------------------------------------------
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-(ul+@10m@b8wl1(%0*=_t^+i9klcy%q#^%jeq!tlefwn@whq3d",
)

DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "hospital-doctor-booking.onrender.com",  # ✅ your live Render domain
]


# ---------------------------------------------------------------------
# APPLICATIONS
# ---------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'crispy_forms',
    'crispy_bootstrap5',

    # Local apps
    'app1',
]

CRISPY_TEMPLATE_PACK = 'bootstrap5'


# ---------------------------------------------------------------------
# MIDDLEWARE
# ---------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ must come right after SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ---------------------------------------------------------------------
# URLS & WSGI
# ---------------------------------------------------------------------
ROOT_URLCONF = 'hospital.urls'
WSGI_APPLICATION = 'hospital.wsgi.application'


# ---------------------------------------------------------------------
# TEMPLATES
# ---------------------------------------------------------------------
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
                'app1.context_processor.first_department',  # ✅ your custom context processor
            ],
        },
    },
]


# ---------------------------------------------------------------------
# DATABASE
# ---------------------------------------------------------------------
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}


# ---------------------------------------------------------------------
# PASSWORD VALIDATION
# ---------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# ---------------------------------------------------------------------
# INTERNATIONALIZATION
# ---------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ---------------------------------------------------------------------
# STATIC FILES (CSS, JS, IMAGES)
# ---------------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []

# ✅ WhiteNoise setup for static files on Render
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ---------------------------------------------------------------------
# DEFAULT PRIMARY KEY FIELD TYPE
# ---------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
