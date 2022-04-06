from .base import *

if os.environ.get('ENVIRONMENT') == 'prod':
   from .prod import *
elif os.environ.get('ENVIRONMENT') == 'test':
   from .test import *
else:
   from .dev import *