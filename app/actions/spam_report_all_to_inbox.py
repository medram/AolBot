import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (TimeoutException,
					JavascriptException,
					NoSuchElementException,
					ElementNotInteractableException
				)


from app.abstract import ActionAbstract
from app import utils, logger

class Spam_report_all_to_inbox(ActionAbstract):

	def apply(self):
		logger.info(f'Processing action ({self.__class__.__name__}) for ({self.isp.profile.email})...')
		driver = self.isp.driver
		profile = self.isp.profile

		# print('Start ActionChains...')
		# Go to Junk section
		driver.get('https://mail.aol.com/')

		# let javascript requests finish.
		time.sleep(5)

		# select navbar items.
		navbar = driver.find_elements_by_css_selector('div.navItem')
		# click on Spam section
		navbar[4].click()
		time.sleep(2)

		# Scroll down.
		with utils.scroll_down(driver, 'div.dojoxGrid-scrollbox', ignored_exceptions=(TimeoutException, JavascriptException)):
			actions = ActionChains(driver)

			time.sleep(1)
			try:
				for _ in range(0, self.isp.get_total_messages(), 1000):
					time.sleep(1)
					# select all msgs.
					checkbox = driver.find_element_by_css_selector('div[dojoattachpoint=headerContentNode] th.dojoxGrid-cell.gridColSel')
					checkbox.click()

					time.sleep(2)
					# mark as not spam
					# ActionChains(driver).send_keys('s').perform()
					divs = driver.find_elements_by_css_selector('div.wsToolbar.dijitBorderContainer-child > div.containerNode > div')
					button_not_spam = divs[10]
					button_not_spam.click()

					try:
						confirm = driver.find_element_by_css_selector('div.modalContainer div[widgetid=uniqName_4_29]')
						confirm.click()
					except NoSuchElementException:
						pass

					# wait to make sure the action is applied
					time.sleep(15)

			except IndexError:
				logger.warning(f'({self.ACTION.name}) action may need an update (IndexError).')
			except ElementNotInteractableException:
				# logger.warning(f'[{self.ACTION.name}] Maybe no messages are found in Spam section of ({profile.email}).')
				logger.info(f'({self.ACTION.name}) {profile.email:.<40} [DONE]')
			except TimeoutException:
				logger.warning(f'[{self.ACTION.name}] Timeout ({profile.email}).')
			except Exception as e:
				logger.exception(f'[{self.ACTION.name}] ({profile.email})')
			else:
				logger.info(f'({self.ACTION.name}) {profile.email:.<40} [DONE]')
