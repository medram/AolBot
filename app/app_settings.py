import os

########################### Global settings ############################

BASE_DIR = os.path.dirname(os.path.dirname(__name__))

DEBUG = True

FIREFOX_PROFILES_PATH = r'C:\Users\%s\AppData\Roaming\Mozilla\Firefox\Profiles' % os.getlogin()

ACCOUNTS_FILE = 'accounts.csv'

DEFAULT_PORT = '3738'

EXECUTABLE_PATH = 'bin/geckodriver.exe'

LOGS_DIR = os.path.join(BASE_DIR, 'logs')

########################### Browser settings  ############################

BROWSER_MINIMIZE_WINDOW = False

########################### Messages settings ############################

MESSAGES_MAX_OPEN 		= 120	# number of messages

MESSAGES_MIN_OPEN 		= 60 	# number of messages

MESSAGES_STARTS_RATIO 	= 0.3 	# from 0 to 1 (0.3 means 30%).

MESSAGES_CLICK_RATIO 	= 0.2 	# from 0 to 1 (0.3 means 30%).

########################### Application info #############################

APP_NAME = 'AolBot'

APP_VERSION = '1.0.0'

POWRED_BY = 'Omega Capital'

DEVELOPED_BY = 'Mohammed Ramouchy'

CONTACT_ME = 'https://github.com/medram'
