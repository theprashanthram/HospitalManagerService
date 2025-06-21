import tempfile

from .base import *

temp_db_file = tempfile.NamedTemporaryFile(suffix='.sqlite3')
TEST_DB_NAME = BASE_DIR / 'db.sqlite3'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': TEST_DB_NAME,
    }
}