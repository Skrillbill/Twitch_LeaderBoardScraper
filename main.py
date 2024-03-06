'''
Leaderboard Scraper
Version 2.x.x
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
from selenium.webdriver.chrome.service import Service
from datetime import datetime

#lets set the defaults
#ini loading
config = configparser.ConfigParser()
config.read('config.ini')
update_conf = config['UPDATER_SETTINGS']



#log init
logging.basicConfig(filename='error.log',encoding='utf-8',filemode='a',level=logging.INFO,format='%(asctime)s: %(levelname)s -> %(message)s')

def update():
    #should probably change this to actually CHECK the version is new rather than blindly download the same version every day...
    logging.info('Checking for updates...')
    url = str(update_conf['chromedriver_latest'])
    if(os.path.isfile('LATEST_RELEASE_STABLE')):
        os.remove('LATEST_RELEASE_STABLE')
        logging.info('removed LATEST_STABLE_RELEASE')

    stableversion = open(wget.download(url),'r').read()
    url = str(update_conf['chromedriver_mirror']) + stableversion + '/win64/chromedriver-win64.zip'

    if(os.path.isfile('chromedriver-win64.zip')):
        os.remove('chromedriver-win64.zip')
        logging.info('removed chromedriver lib')
    stablerelease = wget.download(url)
    shutil.unpack_archive(stablerelease)
    logging.info('Chromedriver has been updated')

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
        logging.info(f'New version detected: {new_version}. Installed version: {current_version}')
        url = str(update_conf['chromedriver_mirror']) + new_version + '/win64/chromedriver-win64.zip'
        stable_release = wget.download(url)
        shutil.unpack_archive(stable_release)
        version_file = open('LATEST_STABLE',"w")
        version_file.write(new_version)
        version_file.close()
        logging.info(f'Chrome driver has been updated to {new_version}')

def scraper():
    # create our headless chrome instance and load the chat page
    stream_url = config['TWITCH_SETTINGS']['Streamer']
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    init_delay = config['SCRAPER_SETTINGS']['delay_init']
    screenshot_delay = config['SCRAPER_SETTINGS']['delay_screenshots']
    try:
        # CHANGE THE EXECUTABLE PATH HERE BELOW THIS LINE(do not need to worry about this i don't think)
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

        time.sleep(screenshot_delay)

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

        time.sleep(screenshot_delay)
        driver.quit()
    except Exception as err:
        logging.critical('%s',err)


def main() -> NoReturn:
    logging.info('Program was initialized')
    update_redux()
    #update()

    #lets get this potty started
    #scraper()




if __name__ == "__main__":
    main()