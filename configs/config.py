import os

TOKEN = os.environ.get('TOKEN')

OPENAI_API = os.environ.get('OPENAI-API')

try:
    from config_dev import *  # noqa
except ImportError:
    pass
