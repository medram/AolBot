import os
import abc
import random
from selenium import webdriver
from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType

# from .utils import MyListeners
from app import common, app_settings


class AbstractISP(abc.ABC):
	def __init__(self, profile):
		self.profile = profile
		# self.list = list_
		# self.task = task
		# self.server = server
		self.driver = self.driver_factory()
		self.loggedin = False
		self.is_created_profile_used = False
		# self.register_actions()

	def driver_factory(self):
		# # get active servers.
		# driver = webdriver.Remote(
		# 			browser_profile=self.profile_factory(),
		# 			command_executor=f'http://{self.server.ip}:{self.server.port}/wd/hub',
		# 			desired_capabilities=(None if self.is_created_profile_used else self.get_capabilities())
		# 		)
		fp = self.profile_factory()
		driver = webdriver.Firefox(
					fp,
					desired_capabilities=(None if self.is_created_profile_used else self.get_capabilities()),
					executable_path=app_settings.EXECUTABLE_PATH,
					service_log_path=os.path.join(app_settings.LOGS_DIR, 'geckodriver.log')
				)

		# driver = EventFiringWebDriver(driver, MyListeners())

		if app_settings.BROWSER_MINIMIZE_WINDOW:
			driver.minimize_window()

		driver.implicitly_wait(10)
		return driver

	def get_capabilities(self):
		capabilities = DesiredCapabilities.FIREFOX.copy()
		# capabilities = DesiredCapabilities.CHROME.copy()
		# print('get_capabilities')
		proxy = self.profile.proxy

		if proxy:
			# print('setting a proxy')
			# print(proxy)
			prox = Proxy()
			prox.proxy_type = ProxyType.MANUAL
			prox.http_proxy = f'{proxy.ip}:{proxy.port}'
			prox.ssl_proxy = f'{proxy.ip}:{proxy.port}'
			prox.ftp_proxy = f'{proxy.ip}:{proxy.port}'

			prox.add_to_capabilities(capabilities)

		# print(capabilities)
		return capabilities


	def get_profile_path(self):
		username = self.profile.email.split('@')[0]

		for profile_path in common.get_profiles_paths():
			if profile_path.endswith(username):
				return profile_path
		return None


	def profile_factory(self):
		profile_path = self.get_profile_path()
		self.is_created_profile_used = False

		if profile_path:
			# return a profile a FireFox profile from this PC
			try:
				fp = webdriver.FirefoxProfile(profile_path)
				self.is_created_profile_used = True
				return fp
			except Exception:
				pass
		# else return a new FireFox profile (by return None)
		return None



	@abc.abstractmethod
	def login(self):
		pass

	@abc.abstractmethod
	def logout(self):
		pass

	def quit(self):
		self.driver.quit()

	@abc.abstractclassmethod
	def register_actions(cls):
		pass



class ActionAbstract(abc.ABC):

	def __init__(self, isp, ACTION):
		self.isp = isp
		self.ACTION = ACTION

	@abc.abstractmethod
	def apply(self):
		pass



# class ISP_Factory():
# 	@staticmethod
# 	def get_isp(profile, l, task, server):
# 		# avoiding circular import.
# 		from selen.ISP.hotmail import Hotmail
# 		from selen.ISP.gmail import Gmail

# 		email = profile.email.lower()
# 		if email.endswith('@hotmail.com') or email.endswith('@outlook.com'):
# 			return Hotmail(profile, l, task, server)

# 		if email.endswith('@gmail.com'):
# 			return Gmail(profile, l, task, server)
