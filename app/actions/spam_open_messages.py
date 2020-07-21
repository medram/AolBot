import time
import random
import click

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, JavascriptException

from app.abstract import ActionAbstract
from app import utils, logger, app_settings, common

class Spam_open_messages(ActionAbstract):

	def apply(self):
		logger.info(f'Processing action ({self.__class__.__name__}) for ({self.isp.profile.email})...')
		driver = self.isp.driver
		profile = self.isp.profile

		# print('Start ActionChains...')
		# Go to spam section.
		driver.get('https://mail.yahoo.com/d/folders/6')

		# let javascript requests finish.
		time.sleep(5)

		# Scroll down.
		with utils.scroll_down(driver, 'div[data-test-id=virtual-list]', ignored_exceptions=(JavascriptException,)):
			time.sleep(2)

			total_messages = self.isp.get_total_messages()

			if not isinstance(total_messages, int):
				# set a default value or exit.
				total_messages = 0

			actions = ActionChains(driver)
			# Archive all messages.
			try:
				# scroll top to open the first message.
				with utils.scroll_up(driver, 'div[data-test-id=virtual-list]', ignored_exceptions=(JavascriptException,)):
					messages = driver.find_elements_by_css_selector('a[data-test-id=message-list-item]')
					messages[0].click()
					# get the amount of messages to open.
					last_message = common.get_amount_of_message(total_messages)
					click.secho(f'({profile.email}) Total messages {total_messages}: {last_message} messages will be openned.', fg='bright_black')

					with click.progressbar(length=last_message, label=f'Openning messages ({profile.email})...', show_pos=True) as bar:
						for i in range(last_message):
							actions = ActionChains(driver)
							actions.send_keys(Keys.ARROW_RIGHT)
							# add start to the current message.
							if random.random() <= app_settings.MESSAGES_STARTS_RATIO:
								actions.send_keys('l')
							actions.perform()

							# show the progress
							# print(f'\r{i+1}/{last_message}', end='')

							bar.update(1) # +=1 each time

							# clear the all chained actions (is not working, it's a bug in selenium source code).
							# actions.reset_actions()

							time.sleep(random.uniform(3, 5))


			except TimeoutException:
				logger.warning(f'({self.ACTION.name}) {profile.email:.<40} [WARNING]')
			except Exception as e:
				logger.exception(f'[{self.ACTION.name}] {profile.email:.<40} [Error]')
			else:
				logger.info(f'({self.ACTION.name}) {profile.email:.<40} [DONE]')
