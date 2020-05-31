import os
from secrets import token_hex

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get("SECRET_KEY", token_hex())

DEBUG = os.environ.get("DEBUG") == "True"

ALLOWED_HOSTS = [os.environ["APP_HOST"]] if "APP_HOST" in os.environ else []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "social_django",
    "graphene_django",
    "graphene_subscriptions",
    "channels",
    "django_celery_results",
    "django_celery_beat",
    "virtualbarcamp.accounts",
    "virtualbarcamp.graphql",
    "virtualbarcamp.home",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "csp.middleware.CSPMiddleware",
]

ROOT_URLCONF = "virtualbarcamp.urls"
GRAPHENE = {"SCHEMA": "virtualbarcamp.graphql.schema.schema"}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "virtualbarcamp", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "virtualbarcamp.webpack.context_processor",
            ],
        },
    },
]

ASGI_APPLICATION = "virtualbarcamp.routing.application"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"console": {"format": "[%(asctime)s] %(levelname)-8s %(name)s: %(message)s"}},
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "console"},
        "null": {"class": "logging.NullHandler"},
    },
    "loggers": {
        "": {"handlers": ["console"], "level": "INFO"},
        "django": {},
        "django.server": {"handlers": ["null"], "level": "INFO", "propagate": False},
    },
}

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT", "5432"),
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [(os.environ.get("REDIS_HOST"), 6379)],},
    },
}

CELERY_RESULT_BACKEND = "django-db"
CELERY_TASK_TRACK_STARTED = True
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_IMPORTS = ["virtualbarcamp.home.signals"]  # Ensure signals are wired up when Celery runs

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTHENTICATION_BACKENDS = ["social_core.backends.discord.DiscordOAuth2"]

SOCIAL_AUTH_DISCORD_KEY = os.environ.get("DISCORD_OAUTH_CLIENT_ID")
SOCIAL_AUTH_DISCORD_SECRET = os.environ.get("DISCORD_OAUTH_CLIENT_SECRET")

LOGIN_REDIRECT_URL = "home"

SOCIAL_AUTH_POSTGRES_JSONFIELD = True

LANGUAGE_CODE = "en-gb"
TIME_ZONE = "Europe/London"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "build"),
    os.path.join(BASE_DIR, "virtualbarcamp", "static"),
]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

WEBPACK_DEV_SERVER_MANIFEST = os.environ.get("WEBPACK_DEV_SERVER_MANIFEST")

if DEBUG:
    CSP_DEFAULT_SRC = ["'self'", "localhost:3000"]
    CSP_SCRIPT_SRC = ["'self'", "localhost:3000", "'unsafe-inline'", "'unsafe-eval'"]
    CSP_STYLE_SRC = ["'self'", "localhost:3000", "'unsafe-inline'", "'unsafe-eval'"]
    CSP_CONNECT_SRC = ["'self'", "localhost:3000", "ws://localhost:3000"]
