import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "8)7)g_l98yj9hrz(kgnsbc#%b86s*gya=%0&u3)8r3b0jx_bnm"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Application definition

INSTALLED_APPS = ["simple"]

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
dbtype = os.environ.get("DBTYPE", "")
if dbtype == "postgres":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "tbench",
            "USER": "postgres",
            "HOST": "127.0.0.1",
            "PORT": "5432",
            "PASSWORD": os.environ.get("PASSWORD"),
        }
    }
elif dbtype == "mysql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "tbench",
            "USER": "root",
            "HOST": "127.0.0.1",
            "PORT": "3306",
            "PASSWORD": os.environ.get("PASSWORD"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "/tmp/db.sqlite3",
        }
    }


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True
