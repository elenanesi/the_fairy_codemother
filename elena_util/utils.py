from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from multiprocessing import Process
from datetime import datetime
import time
import random
import sched
import sys
import tempfile
import os
import json

#location of the chrome driver
CHROME_DRIVER = '/Users/elenanesi/Desktop/Workspace/web-drivers/chromedriver' 
FIREFOX_DRIVER = '/usr/local/bin/geckodriver' 
#define distribution
consent_distribution = {
    'allow-all-button': 70,
    'deny-all-button': 30
}

def log_execution_time(start_time, args):
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Convert start_time from timestamp to datetime
    start_time_formatted = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')

    with open("execution_log.txt", "a") as file:
        file.write(f"Execution time: {elapsed_time:.2f} seconds, Arguments: {args}\n")

    with open("/Users/elenanesi/Workspace/user-simulation/logfile.log", "a") as log_file:
        log_file.write(f"Script executed on {start_time_formatted}\n")
        log_file.write(f"Execution time: {elapsed_time:.2f} seconds\n")

def random_choice_based_on_distribution(distribution_dict):
    """
    Selects an item based on a distribution of probabilities 
    In this script it is called with a distribution from the demo_input.json file as an input

    :param distribution_dict: A dictionary where keys are items to choose from and values are their corresponding probabilities.
    :return: A randomly selected key based on the distribution.
    """
    items = list(distribution_dict.keys())
    weights = list(distribution_dict.values())
    return random.choices(items, weights=weights, k=1)[0]

def consent(driver, page):
    # used to click on cookie banner and give/deny consent to cookies with a 70-30 distribution
    click_class = random_choice_based_on_distribution(consent_distribution)

    try: # wait for page load
        WebDriverWait(driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')
    except TimeoutException:
        print("Timed out waiting for page to load")
        return;

    try:
        # Wait up to 10 seconds for the cookie banner to appear and click on it if does, otherwise throw a TimeoutException
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cookie-banner"))
            )
        link = driver.find_element(By.CLASS_NAME, click_class)
        link.click()
        print(f"consent was given successfully as: {click_class}")
    except TimeoutException:
        print("Timed out waiting for cookie banner to appear");
        return;

def save_client_id(driver):
    # Retrieve cookies
    ga_cookie = driver.get_cookie("_ga")
    ga_1L1YW7SZFP_cookie = driver.get_cookie("_ga_1L1YW7SZFP")

    # Initialize an empty dictionary for client IDs
    data_value = {}

    # Construct the data object
    if ga_cookie and ga_1L1YW7SZFP_cookie:
        data_value = {
            '_ga': ga_cookie['value'],
            '_ga_1L1YW7SZFP': ga_1L1YW7SZFP_cookie['value']
        }
    return data_value

def browser_setup(browser, headless):
    print(f"browser_setup for {browser}")
    if browser == "firefox":
        # Firefox browser setup
        options = FirefoxOptions()
        headless = int(headless)
        if headless == 1:
            options.add_argument("--headless")  # Enables headless mode
        service = FirefoxService(executable_path=FIREFOX_DRIVER)  # Update the path to GeckoDriver
        return webdriver.Firefox(service=service, options=options)
    elif browser == "chrome":
        options = ChromeOptions()
        # Set preferences to automatically allow geolocation requests
        prefs = {
            "profile.default_content_setting_values.geolocation": 1,  # 1: Allow, 2: Block
            "profile.default_content_settings.geolocation": 1,  # Allow geolocation access
        }
        options.add_experimental_option("prefs", prefs)
        
        headless = int(headless)
        if (headless==1):
            options.add_argument("--headless")  # Enables headless mode
        service = ChromeService(executable_path=CHROME_DRIVER)  # Update the path
        return webdriver.Chrome(service=service, options=options)

    driver.execute_script(script)