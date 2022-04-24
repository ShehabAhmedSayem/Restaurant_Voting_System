from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env()
environ.Env.read_env((BASE_DIR / '.env').as_posix())

if env.str('ENV_TYPE') == 'STAGING':
    from .staging import *
elif env.str('ENV_TYPE') == 'PRODUCTION':
    from .production import *
else:
    from .development import *
