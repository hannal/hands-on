from pathlib import Path

from django_jinja.builtins import DEFAULT_EXTENSIONS

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = "django-insecure-144asx^cx(4(x#&)u70z970ga9#uot_#e&e8&)8s+k=8pi7pk="

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd parties
    "django_extensions",
    "django_htmx",
    "django_jinja",
    # Local apps
    "apps.core",
    "apps.product",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "puddingcamp.urls"

TEMPLATES = [
    {
        "BACKEND": "django_jinja.jinja2.Jinja2",
        "DIRS": [
            BASE_DIR / "global_templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "extensions": [
                *DEFAULT_EXTENSIONS,
            ],
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
            "match_extension": ".jinja2",
            "match_regex": None,
            "app_dirname": "templates",
            "newstyle_gettext": True,
            # custom context
            "tests": {},
            "filters": {
                "naturalday": "django.contrib.humanize.templatetags.humanize.naturalday",
                "naturaltime": "django.contrib.humanize.templatetags.humanize.naturaltime",
                "localize": "django.utils.formats.localize",
            },
            "constants": {},
            "globals": {
                "django_htmx_script": "django_htmx.jinja.django_htmx_script",
            },
            "policies": {
                "ext.i18n.trimmed": True,
            },
            "bytecode_cache": {
                "name": "default",
                "backend": "django_jinja.cache.BytecodeCache",
                "enabled": False,
            },
            "autoescape": True,
            "auto_reload": True,
            "translation_engine": "django.utils.translation",
        },
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "puddingcamp.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "_static",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
