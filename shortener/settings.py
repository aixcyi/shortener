"""
shortener 的项目设置。

通过 `Django Template Repo <https://github.com/aixcyi/django-template-repo>`_
模板创建；模板本身使用 Django 4.2.5 通过 'django-admin startproject' 命令生成。

- `settings.py 快速配置 <https://docs.djangoproject.com/zh-hans/4.2/topics/settings/>`_
- `settings.py 完整配置列表 <https://docs.djangoproject.com/zh-hans/4.2/ref/settings/>`_
"""

from pathlib import Path

from utils.converters import dict_

BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / 'logs'
APPS_DIR = BASE_DIR / 'apps'

# -------------------------------- 安全 --------------------------------

# https://docs.djangoproject.com/zh-hans/4.2/ref/settings/#secret-key
SECRET_KEY = None

DEBUG = False

ALLOWED_HOSTS = []  # DEBUG=False 时必须配置为非空列表

APPEND_SLASH = False

# 密码验证
# https://docs.djangoproject.com/zh-hans/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    dict(
        NAME='django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    ),
    dict(
        NAME='django.contrib.auth.password_validation.MinimumLengthValidator',
        OPTIONS={
            "min_length": 8,
        },
    ),
    dict(
        NAME='django.contrib.auth.password_validation.CommonPasswordValidator',
    ),
    dict(
        NAME='django.contrib.auth.password_validation.NumericPasswordValidator',
    ),
]

# -------------------------------- 核心 --------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'apps.core.app_conf.CoreConfig',
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

ROOT_URLCONF = 'shortener.urls'

TEMPLATES = [
    dict(
        BACKEND='django.template.backends.django.DjangoTemplates',
        DIRS=[
            BASE_DIR / 'templates',
        ],
        APP_DIRS=True,
        OPTIONS={
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    ),
]

WSGI_APPLICATION = 'shortener.wsgi.application'

# -------------------------------- 存储 --------------------------------

# 主键字段的默认类型
# 注意：每个app都可以配置app范围内的主键字段默认类型
# https://docs.djangoproject.com/zh-hans/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 用户模型
AUTH_USER_MODEL = 'core.User'

# 数据库
# https://docs.djangoproject.com/zh-hans/4.2/ref/settings/#databases
DATABASES = {
    'template_postgresql': dict(
        ENGINE='django.db.backends.postgresql',
        NAME='<数据库名称>',
        USER='postgres',
        PASSWORD='',
        HOST='127.0.0.1',
        PORT='5432',
    ),
    'template_mysql': dict(
        ENGINE='django.db.backends.mysql',
        NAME='<数据库名称>',
        USER='root',
        PASSWORD='',
        HOST='127.0.0.1',
        PORT='3306',
    ),
    'template_oracle': dict(
        ENGINE='django.db.backends.oracle',
        NAME='<数据库名称>',
        USER='system',
        PASSWORD='',
        HOST='127.0.0.1',
        PORT='1521',
    ),
    'template_sqlite3': dict(
        ENGINE='django.db.backends.sqlite3',
        NAME=BASE_DIR / '[数据库名称].sqlite3',
    ),
}

# 缓存
# https://docs.djangoproject.com/zh-hans/4.2/ref/settings/#caches
CACHES = {
    'template_redis': dict(
        BACKEND='django.core.cache.backends.redis.RedisCache',
        LOCATION='redis://127.0.0.1:6379/0',
    ),
    'template_memory': dict(
        BACKEND='django.core.cache.backends.locmem.LocMemCache',
    ),
}

# 静态文件 (CSS, JavaScript, Images)
# https://docs.djangoproject.com/zh-hans/4.2/howto/static-files/
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'  # 项目app以及项目本身的静态文件将被收集到这个目录，应配置为对外公开的文件路径，例如 /var/www/example.com/static/

# 用户上传内容
# https://docs.djangoproject.com/zh-hans/4.2/topics/security/#user-uploaded-content-security
MEDIA_URL = 'user-uploads/'
MEDIA_ROOT = BASE_DIR / 'media'

# -------------------------------- 国际化 --------------------------------
# Internationalization
# https://docs.djangoproject.com/zh-hans/4.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# -------------------------------- 日志 --------------------------------

# 日志模块的配置：https://docs.djangoproject.com/zh-hans/4.2/topics/logging/#configuring-logging
# 配置字典架构：https://docs.python.org/zh-cn/3/library/logging.config.html#logging-config-dictschema
LOGGING = dict(
    version=1,
    disable_existing_loggers=False,
    formatters={
        # 格式化器默认配置：https://docs.python.org/zh-cn/3/library/logging.html#logging.Formatter
        'verbose': dict(
            format=(
                '[%(asctime)s] '
                '[%(name)s/%(levelname)s] '
                '[%(process)d,%(processName)s] '
                '[%(thread)d,%(threadName)s] '
                '[%(module)s.%(funcName)s:%(lineno)d]: '
                '%(message)s'
            ),
        ),
        'standard': dict(
            format=(
                '[%(asctime)s] '
                '[%(name)s/%(levelname)s] '
                '[%(module)s.%(funcName)s:%(lineno)d]: '
                '%(message)s'
            ),
        ),
        # 自定义格式化器：https://docs.python.org/zh-cn/3/library/logging.config.html#user-defined-objects
        'printing': {
            '()': 'logging.Formatter',
            'fmt': (
                '[%(asctime)s] '
                '[%(name)s/%(levelname)s] '
                '[%(module)s.%(funcName)s:%(lineno)d]: '
                '%(message)s'
            ),
            '.': {
                'default_time_format': '%H:%M:%S',
                'default_msec_format': '%s,%03d',
            },
        }
    },
    filters={
        # 过滤器：https://docs.python.org/zh-cn/3/library/logging.html#logging.Filter
        'require_debugging': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    handlers={
        'Console': dict_(
            class_='logging.StreamHandler',
            level='DEBUG',
            formatter='printing',
        ),
        'RequestRecorder': dict_(
            class_='logging.handlers.TimedRotatingFileHandler',
            level='DEBUG',
            formatter='standard',
            filename=LOGS_DIR / 'requests.log',
            encoding='UTF-8',
            backupCount=365,
            when='d',
        ),
        'ProjectRecorder': dict_(
            class_='logging.handlers.TimedRotatingFileHandler',
            level='DEBUG',
            formatter='standard',
            filename=LOGS_DIR / 'records.log',
            encoding='UTF-8',
            backupCount=365,
            when='d',
        ),
        'ProjectAlarmer': dict_(
            class_='logging.handlers.TimedRotatingFileHandler',
            level='WARNING',
            formatter='verbose',
            filename=LOGS_DIR / 'alarms.log',
            encoding='UTF-8',
            backupCount=365,
            when='d',
        ),
    },
    loggers={
        'django.request': dict(
            level='INFO',
            filters=[],
            handlers=['RequestRecorder'],
            propagate=False,
        ),
        'project': dict(
            level='DEBUG',
            filters=[],
            handlers=['ProjectRecorder', 'ProjectAlarmer'],
            propagate=False,
        ),
    },
)

# -------------------------------- 框架 --------------------------------

# https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = dict(
    DATETIME_FORMAT='%Y-%m-%d %H:%M:%S',
)

# -------------------------------- 其它 --------------------------------

ROOT = 'http://127.0.0.1:65432'
BITS = 4
