from .base import *

if os.environ.get('ENVIRONMENT') == 'prod':
   from .prod import *
else:
   from .dev import *