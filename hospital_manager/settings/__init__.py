import os

env = os.getenv('DJANGO_ENV', 'dev')
if env == 'prod':
    from .test import * # To be updated to actual prod
elif env == 'test':
    from .test import *
else:
    from .dev import *