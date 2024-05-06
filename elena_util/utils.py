from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from multiprocessing import Process
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, date
import time
import random
import sys
import os
import json
import traceback


# Pre-install drivers
ChromeDriverManager().install()
GeckoDriverManager().install()

# location of browser drivers
SHORT_TIME = 2 
LONG_TIME = 5


def color_text(text, color_code):
    # this function is used to beautify log prints
    color = 37 # = white
    if color_code == "red":
        color = 31
    elif color_code == "green":
        color = 32
    elif color_code == "yellow":
        color = 33
    elif color_code == "blue":
        color = 34
    elif color_code == "magenta":
        color = 35
    elif color_code == "cyan":
        color = 36

    return f"\033[{color}m{text}\033[0m"

def log_execution_time(start_time, args):
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Convert start_time from timestamp to datetime
    start_time_formatted = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')

    with open("execution_log.txt", "a") as file:
        file.write(f"Execution time: {elapsed_time:.2f} seconds, Arguments: {args}\n")

def random_choice_based_on_distribution(distribution):
    """
    Selects an item based on a distribution of probabilities 
    In this script it is called with a distribution from the demo_input.json file as an input

    :param distribution: A dictionary where keys are items to choose from and values are their corresponding probabilities.
    :return: A randomly selected key based on the distribution.
    """
    items = list(distribution.keys())
    weights = list(distribution.values())
    return random.choices(items, weights=weights, k=1)[0]

def consent(driver, page, click_class):
    try: # wait for page load
        WebDriverWait(driver, LONG_TIME).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        time.sleep(SHORT_TIME)
        cookie_consent = driver.get_cookie("cookie_consent")
        if cookie_consent is None:
            try:
                # Wait up to 10 seconds for the cookie banner to appear and click on it if does, otherwise throw a TimeoutException
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "cookie-banner"))
                    )
                link = WebDriverWait(driver, SHORT_TIME).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, click_class))
                )
                try:
                    link.click()
                    print(color_text(f"** consent was given successfully as: {click_class}", "green"))
                except(e):
                    print(color_text(f"Cookie banner was not cliccable {e}"), "magenta")
            except TimeoutException:
                print(color_text("** consent(): Timed out waiting for cookie banner to appear", "red"))
                return;
    except TimeoutException:
        print(color_text("** consent(): Timed out waiting for page to load", "red"))
        return;

def save_client_id(driver, ga_cookie_name):
    # Retrieve cookies
    ga_cookie = driver.get_cookie("_ga")
    if ga_cookie is None:
        print(color_text("** ga_cookie is None" , "magenta"))
        return {}  # Return an empty dict or handle as needed

    ga_ID_cookie = driver.get_cookie(ga_cookie_name)

    # Initialize an empty dictionary for client IDs
    data_value = {}

    # Construct the data object
    if ga_cookie and ga_ID_cookie:
        data_value['_ga'] = ga_cookie['value']
        data_value[ga_cookie_name] = ga_ID_cookie['value']
    
    return data_value


def browser_setup(browser, device, headless, process_number):
    print(color_text(f"** {process_number}: I'm starting the browser setup for {browser}", "blue"))
    headless = int(headless)
    if browser == "firefox":
        # Firefox browser setup
        options = FirefoxOptions()       
        if headless == 1:
            options.add_argument("--headless")  # Enables headless mode
        if device == "mobile":
            user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
            window_size = "375,812"  # iPhone X screen resolution in pixels
            options.set_preference("general.useragent.override", user_agent)
            options.add_argument(f"--window-size={window_size}")
        return webdriver.Firefox(options=options)
    elif browser == "chrome":
        options = ChromeOptions()       
        if headless==1:
            options.add_argument("--headless")  # Enables headless mode
        if device == "mobile":
            mobile_emulation = {"deviceName": "iPhone X"}
            options.add_experimental_option("mobileEmulation", mobile_emulation)
        return webdriver.Chrome(options=options)
        
# end of file