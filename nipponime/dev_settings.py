# Configurações específicas para desenvolvimento
# Este ficheiro pode ser usado para sobrepor configurações em desenvolvimento

import os
from .settings import *

# Configurações de desenvolvimento
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Base de dados SQLite para desenvolvimento
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'nipo.sqlite3',
    }
}

# Configurações de email para desenvolvimento (console backend)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Configurações de ficheiros estáticos para desenvolvimento
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_URL = '/images/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')
