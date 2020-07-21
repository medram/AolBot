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

class Inbox_open_messages(ActionAbstract):

	def apply(self):
		logger.info(f'Processing action ({self.__class__.__name__}) for ({self.isp.profile.email})...')
		driver = self.isp.driver
		profile = self.isp.profile

		# Go to Inbox section
		driver.get('https://mail.aol.com/')

		# let javascript requests finish.
		time.sleep(5)

		# select navbar items.
		navbar = driver.find_elements_by_css_selector('div.navItem')
		# click on Inbox section
		navbar[1].click()
		time.sleep(2)

		total_messages = self.isp.get_total_messages()

		if not isinstance(total_messages, int):
			# set a default value or exit.
			total_messages = 0

		actions = ActionChains(driver)
		# Archive all messages.
		try:
			if total_messages == 0:
				logger.warning(f'({self.ACTION.name}) Maybe no messages are found in spam section of ({profile.email})')
			else:
				# clicking the first messages.
				driver.execute_script("""
					let messages_row = document.querySelectorAll("div.dojoxGrid-content div.dojoxGrid-row")
					messages_row[0].classList.add("dojoxGrid-row-over")
				""")
				ActionChains(driver).send_keys(Keys.ENTER).perform()

				# get the amount of messages to open.
				last_message = common.get_amount_of_message(total_messages)
				click.secho(f'({profile.email}) Total messages {total_messages}: {last_message} messages will be openned.', fg='bright_black')

				with click.progressbar(length=last_message, label=f'Openning messages ({profile.email})...', show_pos=True) as bar:
					for i in range(last_message):
						actions = ActionChains(driver)
						actions.send_keys('n')
						# add start to the current message.
						if random.random() <= app_settings.MESSAGES_STARTS_RATIO:
							try:
								button_flag = driver.find_element_by_css_selector('span.flag')
								button_flag.click()
							except Exception:
								logger.warning('Cannot add Flags to messages, it may need a fix!')
						actions.perform()

						# show the progress
						# print(f'\r{i+1}/{last_message}', end='')
						bar.update(1) # +=1 each time

						# clear the all chained actions (is not working, it's a bug in selenium source code).
						# actions.reset_actions()

						time.sleep(random.uniform(3, 5))


		except TimeoutException:
			logger.warning(f'({self.ACTION.name}) {profile.email}')
		except Exception as e:
			logger.exception(f'({self.ACTION.name}) {profile.email}')
		else:
			logger.info(f'({self.ACTION.name}) {profile.email:.<40} [DONE]')
