import os

DATABASE = os.path.join(
    os.path.abspath(
        os.path.dirname(__file__)),
    'task-manager.db')
CONFIG = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.ini')
LOGGING_ENABLED = True
LOGS_DIRECTORY = '/var/tmp' if os.path.exists(
    '/var/tmp') else os.environ['HOME']
HIGH_LEVEL_LOG_NAME = 'high.log'
LOW_LEVEL_LOG_NAME = 'low.log'
LOGGING_FORMATTER = '%(asctime)s, %(name)s, [%(levelname)s]: %(message)s'
