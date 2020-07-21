import os
import logging
import colorlog


from app import app_settings

LOG_FILE = os.path.join(app_settings.LOGS_DIR, 'errors.log')

# make sure logs file exists
if not os.path.isdir(app_settings.LOGS_DIR):
	os.makedirs(app_settings.LOGS_DIR)

# default logger.
logger = logging.getLogger(__name__)
# make it DEBUG level to let thandlers more comfortable.
logger.setLevel(logging.DEBUG)

# Adding console logging.
c_handler = colorlog.StreamHandler()
# c_formater = logging.Formatter('[%(levelname)s] - %(message)s')
c_formater = colorlog.ColoredFormatter(
				'%(log_color)s[%(levelname)s] - %(message)s',
				log_colors={
						'DEBUG':    'bold_black',
						'INFO':     'cyan',
						'WARNING':  'yellow',
						'ERROR':    'red',
						'CRITICAL': 'bold_red',
					},
				)
c_handler.setFormatter(c_formater)
c_handler.setLevel(logging.DEBUG if app_settings.DEBUG else logging.INFO)

# Adding file logging.
f_handler = logging.FileHandler(LOG_FILE)
f_formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] \t- %(message)s')
f_handler.setFormatter(f_formatter)
f_handler.setLevel(logging.WARNING)

# logger = colorlog.getLogger()

# register handlers
logger.addHandler(c_handler)
logger.addHandler(f_handler)
