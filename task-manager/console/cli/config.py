import os


APP_DATA_DIRECTORY = os.path.join(os.environ['HOME'], 'task-manager')
DATABASE = os.path.join(APP_DATA_DIRECTORY, 'task-manager.db')
CONFIG_FILE = os.path.join(APP_DATA_DIRECTORY, 'config.ini')
LOGGING_ENABLED = True
LOGS_DIRECTORY = APP_DATA_DIRECTORY
LOG_FILE = 'log.log'
LOG_ALL_LEVELS = True
LOG_FORMAT = '%(asctime)s, %(name)s, [%(levelname)s]: %(message)s'
