from django.conf import settings
from os import getenv
from dotenv import load_dotenv

load_dotenv(settings.BASE_DIR.parent / "env/memorize.env")

SECRET_KEY = getenv("SECRET_KEY")
ALLOWED_HOSTS = getenv("ALLOWED_HOSTS").split(" ")

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # own 
    'account',
    'school',

    # third party
    "django_htmx",
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

    # third party middleware
    "django_htmx.middleware.HtmxMiddleware",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': settings.BASE_DIR.parent / "data/memorize.sqlite3",
    }
}