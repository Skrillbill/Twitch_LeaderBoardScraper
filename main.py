'''
Leaderboard Scraper
Version 2.0.2
SkrillBill
https://github.com/SkrillBill
'''
from typing import NoReturn
import configparser
import shutil
import pycurl
import requests
import wget
import os
import logging
import time
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException , WebDriverException
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

#log init
logging.basicConfig(filename='error.log',encoding='utf-8',filemode='a',level=logging.INFO,format='%(asctime)s: %(levelname)s -> %(message)s')
#lets set the defaults
#ini loading
try:
    if(os.path.isfile('config.ini')):
        config = configparser.ConfigParser()
        config.read('config.ini')
        update_conf = config['UPDATER_SETTINGS']

    else:
        logging.critical('INI file is not detected. Please download it at https://github.com/Skrillbill/Twitch_LeaderBoardScraper/blob/master/config.ini')
except NameError as err:
    logging.critical(f'Variable Error: {err}')
except Exception as err:
    logging.critical(f'Something went wrong: {err}')




def update_redux():
    current_version = "0"
    latest_url = str(update_conf['chromedriver_latest'])
    if(os.path.isfile('LATEST_STABLE')): # current_version defaults to none/0. But if we've updated before, we'll override the variable with whatvever the last downloaded version was.
        with open('LATEST_STABLE') as lrs:
            current_version = lrs.read()

    # google for testing has a json endpoint we can query for the current version of all the release channels. We only care about Stable
    response = requests.get(str(config['UPDATER_SETTINGS']['chromedriver_version']))
    data = response.json()
    new_version = json.dumps(data.get('channels').get('Stable').get('version'))
    new_version = new_version.strip('"') #strip the quotation marks from the json string

    if str(current_version) == str(new_version) : #is already current version
        logging.info(f'No update required: Current: {current_version} and new version {new_version}')
    else: #download new version
        logging.info(f'New version detected: {new_version}. Installed version: {current_version}...Updating')
        url = str(update_conf['chromedriver_mirror']) + new_version + '/win64/chromedriver-win64.zip'
        stable_release = wget.download(url)
        shutil.unpack_archive(stable_release)

        version_file = open('LATEST_STABLE',"w")
        version_file.write(new_version)
        version_file.close()

        logging.info(f'Chromedriver has been updated to {new_version}')


def popup_window(message):
    root = tk.Tk()
    root.withdraw() #so we don't display the full GUI; we only need message box
    messagebox.showinfo("Twitch Scraper Notification", message)
    root.destroy()



def scraper():
    status_state = "Fail"
    watchdog_popup = bool(config['SCRAPER_SETTINGS']['show_popup'])
    # create our headless chrome instance and load the chat page
    stream_url = config['TWITCH_SETTINGS']['Streamer']
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    init_delay = int(config['SCRAPER_SETTINGS']['delay_init'])
    screenshot_delay = int(config['SCRAPER_SETTINGS']['delay_screenshots'])
    try:
        chrome_service = Service('chromedriver-win64\chromedriver.exe')
        driver = webdriver.Chrome(service=chrome_service)
        driver.get(stream_url)

        # wait for initial page load
        time.sleep(init_delay)

        # set some defaults
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_")
        gifters = timestamp + "top_gifter.png"
        bittys = timestamp + "top_bittys.png"


        # here we find the rotate leaderboard butotn and click it, expand it, screenshot it, rotate it again, and screenshot again.
        rotate_button = driver.find_element("xpath",
                                            '//*[@id="root"]/div/div[1]/div/div/section/div/div[1]/div/div/div/div/div/div/div[3]/button')
        rotate_button.click()
        time.sleep(screenshot_delay)

        expand_sublb_button = driver.find_element("xpath",
                                                  '/html/body/div[1]/div/div[1]/div/div/section/div/div[1]/div/div/div/div/div/div/div[2]/button')
        expand_sublb_button.click()
        time.sleep(screenshot_delay)
        driver.get_screenshot_as_file(str(config['SCRAPER_SETTINGS']['output_dir']) + bittys)
        logging.info(str(config['SCRAPER_SETTINGS']['output_dir']) + bittys)
        time.sleep(screenshot_delay)

        rotate_button = driver.find_element("xpath",
                                            '//*[@id="root"]/div/div[1]/div/div/section/div/div[1]/div/div/div/div/div/div[1]/div[2]/button')
        rotate_button.click()
        time.sleep(screenshot_delay)
        driver.get_screenshot_as_file(str(config['SCRAPER_SETTINGS']['output_dir']) + gifters)
        logging.info(str(config['SCRAPER_SETTINGS']['output_dir']) + gifters)

        driver.quit()
        status_state = 'Success'


    except NoSuchElementException as e:
        logging.critical('Button does not exist. (most common cause is no subs or bits at start of month) : ')
        logging.critical('%s',e)


    except WebDriverException as e:
        logging.critical('WebDriver error: ')
        logging.critical('%s', e)


    except Exception as err:
        logging.critical('Something went wrong.. try again or open a ticket at https://github.com/Skrillbill/Twitch_LeaderBoardScraper')
        logging.critical('%s',err)

    finally:
        logging.info('Script Execution finished. Status: %s', status_state)
        if (watchdog_popup == True):
            popup_window(f'Execution was a {status_state}.')



def main() -> NoReturn:
    logging.info('Program was initialized')
    update_redux()
    scraper()


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        logging.critical(f'Something unexpected happened:  {err}')