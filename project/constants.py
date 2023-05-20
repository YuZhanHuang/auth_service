import os
from enum import Enum, auto

LOG_PATH = os.environ.get('LOGGER_PATH', '/app/logs')
LOG_FILE = os.environ.get('LOG_FILE', 'auth_service')
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
LOCAL_TZ = 'Asia/Taipei'
DEFAULT_PASSWORD = '12345678'

