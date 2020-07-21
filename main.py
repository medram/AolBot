import sys
import traceback
import logging
import time
import click

from selenium.common.exceptions import WebDriverException

from app import Aol, common, logger, app_settings

# messages = list(range(10))
# total_messages = len(messages)
# print(click)
# with click.progressbar(messages,
# 						label='Openning messages...',
# 						length=total_messages,
# 						show_pos=True,
# 						color='green') as bar:
#     for x in bar:
#         time.sleep(0.5)
# exit()

# main function.
def main():
	# show an introduction about YahooBot
	common.show_introduction()

	try:
		profiles_list = common.load_profiles_from_csv()
	except FileNotFoundError:
		logger.error(f'Oops! "{app_settings.ACCOUNTS_FILE}" file not found.')
		exit(1)
	# ACTION = common.get_action()
	ACTIONS = common.get_actions()

	logger.debug(f'Total emails: {len(profiles_list)}')

	start = time.time()



	try:
		# logger.info(f'Processing ({ACTION.name}) ...')
		for i, profile in enumerate(profiles_list):
			logger.debug(f'Emails processed: {i}/{len(profiles_list)} ({round(i / len(profiles_list) * 100, 2)}%)')
			try:
				isp = Aol(profile)
				isp.login()
				# invoke multiple actions.
				for ACTION in ACTIONS:
					try:
						isp.do_action(ACTION)
					except WebDriverException as e:
						if 'Message: Reached error page' in str(e):
							logger.warning(f'Please check your internet connection of your server/RDP')
						elif 'Message: Failed to decode response' in str(e):
							logger.warning(f'Message: Failed to decode response from marionette!')
						elif 'Message: permission denied' in str(e):
							logger.warning(f'Message: permission denied!')
						else:
							logger.exception('Exception occured')
				isp.quit()

			except WebDriverException as e:
				if 'Message: Reached error page' in str(e):
					logger.warning(f'Please check your internet connection of your server/RDP')
				elif 'Message: Failed to decode response' in str(e):
					logger.warning(f'Message: Failed to decode response from marionette!')
				elif 'Message: permission denied' in str(e):
					logger.warning(f'Message: permission denied!')
				else:
					logger.exception('Exception occured')
			except KeyboardInterrupt:
				raise
			except Exception as e:
				# exc_type, exc_value, exc_tb = sys.exc_info()
				# traceback.print_exception(exc_type, exc_value, exc_tb)
				logger.exception('Exception occured')

		logger.debug(f'{len(profiles_list)} emails have been processed in ({common.prettify_seconds(time.time() - start)})')
	except KeyboardInterrupt:
		logger.info('Stopped')


if __name__ == '__main__':
	main()
