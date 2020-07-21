import time
import json
import os
# import pickle

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
		NoSuchElementException,
		ElementClickInterceptedException,
		InvalidCookieDomainException,
		StaleElementReferenceException,
		TimeoutException
	)

from app.logger import logger
from app.abstract import AbstractISP, ActionAbstract
from app import exceptions, utils, app_settings
from app.common import Actions
from app.actions import (
		Spam_report_all_to_inbox,
		Inbox_archive_all,
		Inbox_open_messages,
		Spam_open_messages,
		Inbox_open_plus_click_messages
	)


class Aol(AbstractISP):
	actions = {}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def do_action(self, ACTION):
		if self.loggedin:
			# self.driver.get('https://mail.Aol.com')
			self.driver.implicitly_wait(4)
			# let javascript requests finish.
			time.sleep(3)
			try:
				ActionObject = self.actions[ACTION](self, ACTION)
				if isinstance(ActionObject, ActionAbstract):
					ActionObject.apply()
			except KeyError:
				pass
			# except Exception as e:
			# 	print(e)


	@classmethod
	def register_actions(cls, actions):
		for action, action_class in actions:
			cls.actions[action] = action_class

		# cls.actions[Actions.SPAM_REPORT_ALL_TO_INBOX] = Spam_report_all_to_inbox(self)
		# cls.actions[Actions.INBOX_SELECT_ALL_MARK_AS_READ] = Inbox_select_all_mark_as_read(self)
		# cls.actions[Actions.SPAM_SELECT_ALL_MARK_AS_READ] = Spam_select_all_mark_as_read(self)
		# cls.actions[Actions.INBOX_ARCHIVE_ALL] = Inbox_archive_all(self)
		# cls.actions[Actions.INBOX_OPEN_MESSAGES] = Inbox_open_messages(self)

	@classmethod
	def get_available_actions(cls):
		return tuple(cls.actions.keys())


	def login(self):
		self._automatic_login()


	def logout(self):
		pass


	def create_profile(self):
		print('creating profile.')

	def get_total_messages(self):
		return self.driver.execute_script("""
			let el = document.querySelector('div#uniqName_5_2')
			return parseInt(el.innerText.split(' ').pop().slice(1, -1))
		""")


	def _automatic_login(self):
		self.driver.get('https://mail.aol.com')
		self.driver.implicitly_wait(3)
		time.sleep(5)

		# check the login.
		if self.driver.current_url.startswith('https://login.aol.com'):
			self.loggedin = False
			logger.info('{} (automatic login...).'.format(self.profile.email))

			email = self.driver.find_element_by_id("login-username")
			email.clear()
			email.send_keys(self.profile.email)
			email.send_keys(Keys.RETURN)

			self.driver.implicitly_wait(3)
			time.sleep(3)

			password = self.driver.find_element_by_id('login-passwd')
			password.clear()
			password.send_keys(self.profile.password)

			time.sleep(1)
			# Click login
			try:
				password.send_keys(Keys.RETURN)
			except StaleElementReferenceException:
				self.driver.find_element_by_id('login-signin').click()

			self.driver.implicitly_wait(2)
			time.sleep(2)

			self.driver.get('https://mail.aol.com')
			time.sleep(2)

			# check the login status.
			try:
				wait = WebDriverWait(self.driver, 30, poll_frequency=0.05)
				wait.until(EC.url_contains('https://mail.aol.com'))
			except TimeoutException:
				logger.warning('{} (May need a manual login).'.format(self.profile.email))
				raise exceptions.CantLogin()

			# report that we are logged in :D
			self.loggedin = True
		else:
			# report that we are logged in :D
			self.loggedin = True


# set the available actions.
available_actions = [
	(Actions.SPAM_REPORT_ALL_TO_INBOX, Spam_report_all_to_inbox),
	(Actions.INBOX_ARCHIVE_ALL, Inbox_archive_all),
	(Actions.INBOX_OPEN_MESSAGES, Inbox_open_messages),
	(Actions.SPAM_OPEN_MESSAGES, Spam_open_messages),
	(Actions.INBOX_OPEN_PLUS_CLICK_MESSAGES, Inbox_open_plus_click_messages),
]

# registring all Aol actions here.
Aol.register_actions(available_actions)

