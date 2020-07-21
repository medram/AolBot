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

class Inbox_open_plus_click_messages(ActionAbstract):

	def apply(self):
		logger.info(f'Processing action ({self.__class__.__name__}) for ({self.isp.profile.email})...')
		driver = self.isp.driver
		profile = self.isp.profile

		# print('Start ActionChains...')
		# Go to Inbox section
		driver.get('https://mail.yahoo.com/d/folders/1')

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

							# perform actions in the chain.
							actions.perform()
							time.sleep(1)
							# click on an image (first image) in the current message.
							if random.random() <= app_settings.MESSAGES_CLICK_RATIO:
								# driver.execute_script("""
								# 	let images = document.querySelectorAll("div[data-test-id=message-view-body-content] a img")
								# 	if (images.length)
								# 		images[0].click()
								# """)

								images_in_messages = driver.find_elements_by_css_selector('div[data-test-id=message-view-body-content] a img')
								if images_in_messages:
									# try:
									image_to_click = images_in_messages[0]
									ActionChains(driver).key_down(Keys.CONTROL).click(image_to_click).key_up(Keys.CONTROL).perform()
								# 	print(image_to_click)
								# 	# image_to_click.click()
								# 	actions.pause(1).click(image_to_click)
								# 	# actions.move_to_element(image_to_click).click(image_to_click)
								# 	# except Exception:
								# 	# 	pass

							bar.update(1) # +=1 each time

							time.sleep(random.uniform(2, 5))

			except TimeoutException:
				logger.warning(f'({self.ACTION.name}) {profile.email:.<40} [WARNING]')
			except Exception as e:
				logger.exception(f'[{self.ACTION.name}] {profile.email:.<40} [Error]')
			else:
				logger.info(f'({self.ACTION.name}) {profile.email:.<40} [DONE]')
