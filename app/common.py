import os
import csv
import click
import random
from enum import Enum

from app import app_settings

class Singleton:
	def __init__(self, cls):
		self._cls = cls

	def get_instance(self):
		try:
			return self._instance
		except AttributeError:
			self._instance = self._cls()

		return self._instance

	def __call__(self):
		raise TypeError('Singletons must be accessed through `get_instance()`.')

	def __instancecheck__(self, inst):
		return isinstance(inst, self._cls)


def get_profiles_paths():
	return [
            os.path.join(app_settings.FIREFOX_PROFILES_PATH, d) for d in os.listdir(app_settings.FIREFOX_PROFILES_PATH)
            if os.path.isdir(os.path.join(app_settings.FIREFOX_PROFILES_PATH, d))
            and 'default' not in d
        ]


class Profile:
	def __init__(self, email, password, proxy=None):
		self.email = email
		self.password = password
		self.proxy = proxy

	def __repr__(self):
		return f'<Profile {self.email}>'

class List:
	def __init__(self):
		self.profiles = None


class Proxy:
	def __init__(self, ip, port=app_settings.DEFAULT_PORT):
		self.ip = ip
		self.port = port

	def __repr__(self):
		return f'<Proxy {self.ip}>'


class Actions(Enum):
	SPAM_REPORT_ALL_TO_INBOX		= 0
	INBOX_SELECT_ALL_MARK_AS_READ	= 1
	SPAM_SELECT_ALL_MARK_AS_READ	= 2
	INBOX_ARCHIVE_ALL				= 3
	INBOX_OPEN_MESSAGES				= 4
	SPAM_OPEN_MESSAGES				= 5
	INBOX_OPEN_PLUS_CLICK_MESSAGES	= 6


def load_profiles_from_csv():
	profiles_list = []
	with open(app_settings.ACCOUNTS_FILE) as f:
		reader = csv.DictReader(f)
		for line in reader:
			# create profile, proxy.
			proxy = None
			if line['proxy']:
				parts = line['proxy'].split(':')
				if len(parts) == 2:
					ip, port = parts
					proxy = Proxy(ip, port)
				else:
					proxy = Proxy(parts[0])

			if proxy:
				profile = Profile(line['email'], line['password'], proxy)
			else:
				profile = Profile(line['email'], line['password'])
			profiles_list.append(profile)
	return profiles_list


def show_introduction():
	introduction = f"""
+----------------------------------------------------------------------------+
|                                                                            |
|     █████╗  ██████╗ ██╗         ██████╗  ██████╗ ████████╗                 |
|    ██╔══██╗██╔═══██╗██║         ██╔══██╗██╔═══██╗╚══██╔══╝                 |
|    ███████║██║   ██║██║         ██████╔╝██║   ██║   ██║                    |
|    ██╔══██║██║   ██║██║         ██╔══██╗██║   ██║   ██║                    |
|    ██║  ██║╚██████╔╝███████╗    ██████╔╝╚██████╔╝   ██║                    |
|    ╚═╝  ╚═╝ ╚═════╝ ╚══════╝    ╚═════╝  ╚═════╝    ╚═╝                    |
|                                                                            |
|                                                                            |
|    {app_settings.APP_NAME} v{app_settings.APP_VERSION}                      Developed By: {app_settings.DEVELOPED_BY}      |
|                                                                            |
|    Powred By: Omega Capital.          Contact: {app_settings.CONTACT_ME}   |
|                                                                            |
+----------------------------------------------------------------------------+

"""
	click.secho(introduction, fg='bright_black')


def show_actions_list():
	actions = get_available_actions()
	h1 = ' Aol actions list:'
	click.secho(h1, fg='cyan')
	click.secho('-' * len(h1), fg='cyan')

	for i, action in enumerate(actions, 1):
		action_string_parts = action.name.split('_')
		action_pos = action_string_parts[0]
		action_name = '_'.join(action_string_parts[1:])
		print(f' {i} - ({action_pos}) {action_name}')


def get_action():

	actions = get_available_actions()
	show_actions_list()
	try:
		click.secho('\nPlease choose the action you want ? (Ctrl+C to exit): ', fg='yellow', nl=False)
		num = int(input())
		while num < 1 or num > len(actions):
			click.secho('Opps!, Action not found.', fg='red')
			click.secho('Please choose an action from the list above ? (Ctrl+C to exit): ', fg='yellow', nl=False)
			num = int(input())
	except KeyboardInterrupt:
		exit()
	return actions[num - 1]


def get_actions():
	actions = get_available_actions()
	result = []
	show_actions_list()
	try:
		click.secho('\nPlease choose actions you want ? (Ctrl+C to exit): ', fg='yellow', nl=False)
		actions_string = [ int(n) for n in str(input()).split(' ')]
		for num in actions_string:
			while num < 1 or num > len(actions):
				click.secho(f'Opps!, Action {num} not found.', fg='red')
				exit()
				# click.secho('Please choose actions from the list above ? (Ctrl+C to exit): ', fg='yellow', nl=False)
				# num = int(input())
			result.append(actions[num - 1])
	except KeyboardInterrupt:
		exit()
	return result


def get_available_actions():
	from app import Aol
	return Aol.get_available_actions()


def get_mailbox_messages_range(total_messages):
	""" Get the max and min messages in the inbox """
	x_min = min(total_messages, app_settings.MESSAGES_MIN_OPEN)
	x_max = min(total_messages, app_settings.MESSAGES_MAX_OPEN)
	return x_min, x_max

def get_amount_of_message(total_messages):
	"""Get the amount of messages to open."""
	return random.randint(*get_mailbox_messages_range(total_messages))


def prettify_seconds(sec):
	if sec < 60: 		# less than 1 minute.
		return '%.2f seconds' % sec
	elif sec / 60 < 60: # less than 1 hour.
		return '%.2f minutes' % (sec / 60)
	elif sec / 3600 < 24: # less than 1 day.
		return '%.2f hours' % (sec / 3600)

	# return in days.
	return '%.2f days' % (sec / 86400)

