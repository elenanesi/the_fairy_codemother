from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
from multiprocessing import Process
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, date
from codecarbon import EmissionsTracker
import time
import random
import sys
import os
import json
import traceback
import requests
import subprocess
import threading
import argparse
import xml.etree.ElementTree as ET

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

def get_cookie(page, cookie_name):
    # Retrieve all cookies from the page
    cookies = page.context.cookies()
    # Iterate through cookies to find the specific one
    for cookie in cookies:
        if cookie['name'] == cookie_name:
            return cookie['value']
    return None  # Return None if cookie is not found

def consent(page, process_number, url, click_class):
    try: # wait for page load
        cookie_consent = get_cookie(page, "cookie_consent")
        if cookie_consent is None:
            time.sleep(SHORT_TIME)
            page.wait_for_selector(".cookie-banner", timeout=5000)
            consent_button = page.wait_for_selector(f".{click_class}", timeout=5000)
            consent_button.click()
            print(color_text(f"** {process_number}: consent was given successfully as: {click_class}", "green"))
    except(e):
        print(color_text(f"Cookie banner was not cliccable {e} at {url}"), "magenta")

def browser_setup(browser_input, device, headless, process_number):
    print(color_text(f"** {process_number}: I'm starting the browser setup for {browser_input} with headless {headless}", "blue"))
    if device == "mobile":
        if browser_input == "firefox":
            # use iphone and safari
            user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
        else:
            user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"

    else: 
        # chrome desktop
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        if browser_input == "firefox":
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
        
    # geolocation = {'latitude': 37.7749, 'longitude': -122.4194} 
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch( headless=headless)
    context = browser.new_context(user_agent=user_agent)
    # context.set_geolocation(geolocation)
    return browser, context
        
# end of file