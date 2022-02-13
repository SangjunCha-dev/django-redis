from .base import *


SECRET_BASE_FILE = os.path.join(CONFIG_BASE_DIR, 'secrets/secrets.json')
secrets = json.loads(open(SECRET_BASE_FILE).read())
for key, value in secrets.items():
    setattr(sys.modules[__name__], key, value)

DEBUG = True

ALLOWED_HOSTS = [
    '*',
]

SIMPLE_JWT['SIGNING_KEY'] = SECRET_KEY

# 외부 스토리지 지정
if system() == 'Windows':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    # Redis
    CACHES = {
        'default': {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://redis_cache",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }