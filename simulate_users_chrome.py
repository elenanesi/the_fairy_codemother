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
from concurrent.futures import ProcessPoolExecutor



#from elena_util import *


# --- GLOBAL VARS ---- #


# page category options
#define distribution
consent_distribution = {
    'allow-all-button': 70,
    'deny-all-button': 30
}
#where to save client ids
SHORT_TIME = 1
LONG_TIME = 10
client_ids_file = '/Applications/MAMP/htdocs/demo_project/client_ids.json'
#page category options
page_categories = ["home", "category", "product"]
# product category options
product_categories = ["apples", "kiwis", "oranges"]
# path options
path_functions = ["bounce","engaged", "product", "add_to_cart"]
# run headless by default
HEADLESS = 1
# number of users and sessions to run at every execution of the script
NR_USERS = 100
#location of the chrome driver
CHROME_DRIVER = '/Users/elenanesi/Desktop/Workspace/web-drivers/chromedriver' 
FIREFOX_DRIVER = '/usr/local/bin/geckodriver' 
# Base URL for navigation, my localhost website
base_url = "http://www.thefairycodemother.com/demo_project/"
# get info from demo_input.json file to get the necessary input for paths (CVR and distribution)
os.chdir('/Users/elenanesi/Workspace/user-simulation/')
if os.path.exists("demo_input.json"):
    with open("demo_input.json", 'r') as file:
        demo_input = json.load(file)
else:
    print ("demo_input.json is missing!!")
    with open("/Users/elenanesi/Workspace/user-simulation/logfile.log", "a") as log_file:
        log_file.write(f"Script failed because demo_input.json is missing. Executed on {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

# ---- end of global vars --- #

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
    
def save_user_id(driver):
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


def get_landing_page(driver, source):
    # Setup of landing page
    utm_parameters = ""
    if (source != "direct"):
        if "organic" in source:
            utm_parameters="?utm_source=" + demo_input[source]['source'] + "&utm_medium=" + demo_input[source]['medium']
        else:
            utm_parameters="?utm_source=" + demo_input[source]['source'] + "&utm_medium=" + demo_input[source]['medium'] + "&utm_campaign=" + demo_input[source].get('campaign', '')
    print(f"Selected utms: {utm_parameters}")
    page = random.choice(page_categories)  # Choosing a random page category
    

    # Assign a random landing page
    if page == "product":
        # Choose a random category for the product
        category = random.choice(product_categories)
        # Generate a random product ID between 1 and 10
        product_id = str(random.randint(1, 3))
        # Construct and navigate to the product URL
        url = f"{base_url}{category}/{product_id}.php{utm_parameters}"
        driver.get(url)
        return url

    elif page == "category":
        # Choose a random category
        category = random.choice(product_categories)
        # Navigate to the category URL
        url = f"{base_url}{category}.php{utm_parameters}"
        driver.get(url)
        return url

    else:
        # Navigate to a generic page URL
        url = f"{base_url}{page}.php{utm_parameters}"
        driver.get(url)
        return url

def add_to_cart(driver):
    category = random.choice(product_categories)
    product_id = str(random.randint(1, 3))
    url = f"{base_url}{category}/{product_id}.php"
    purchase_prm = f"?cat={category}&prod={product_id}"
    driver.get(url)
    try: 
        WebDriverWait(driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        print("got to product page")
        try:
            link = driver.find_element(By.CLASS_NAME, "cart")
            link.click()
            print("Added to cart.")
            time.sleep(5)
            return purchase_prm
        except Exception as e:
            print(f"An error occurred w add to cart click on {url}: {e}")
            return purchase_prm

    except TimeoutException:
        print("product page did not load")
        return purchase_prm

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


def execute_purchase_flow(browser, source, headless):
    # vars
    temp_client_ids = {}
    client_ids = []
    global HEADLESS

	## TO ADD: PURCHASE VERSION: NEW/RETURNING CLIENT, FROM BEGINNING OR FROM ADD TO CART OR OTHER?
    print("--execute_purchase_flow fired")

    # Define browser; 
    driver = browser_setup(browser, headless)

    # Setup of utms
    utm_parameters = ""
    if (source != "direct"):
        if "organic" in source:
            utm_parameters="?utm_source=" + demo_input[source]['source'] + "&utm_medium=" + demo_input[source]['medium']
        else:
            utm_parameters="?utm_source=" + demo_input[source]['source'] + "&utm_medium=" + demo_input[source]['medium'] + "&utm_campaign=" + demo_input[source].get('campaign', '')
    print(f"Selected utms: {utm_parameters}")
    
    # Add navigation actions here

    # url is landing page
    url = "http://www.thefairycodemother.com/demo_project/home.php"+ utm_parameters
    driver.get(url)  # Your website URL

    # Give/deny consent
    consent(driver, url)
    # save device_id in file to reuse later
    # Load existing cookie pairs from file, if it exists
    try:
        if os.path.exists(client_ids_file):
            with open(client_ids_file, 'r') as file:
                client_ids = json.load(file)

        if len(client_ids)<150: #limit the client_ids to 150ish in total to avoid the machine from exploding while calculating length
            temp_client_ids = save_user_id(driver)

    except Exception as e:
        print(f"Error with client_ids.json because: {e}")

    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Stay on the page for 5 seconds and go to the next page
    time.sleep(SHORT_TIME)
    purchase_prm = add_to_cart(driver)
    time.sleep(SHORT_TIME)  
    driver.get("http://www.thefairycodemother.com/demo_project/checkout.php"+purchase_prm)
    print("begin checkout")
    time.sleep(SHORT_TIME)  
    driver.get("http://www.thefairycodemother.com/demo_project/purchase.php"+purchase_prm)
    time.sleep(LONG_TIME) 
    print("purchase happened")

    driver.quit()

def execute_browsing_flow(browser, source, headless):
    #global temp_client_ids
    temp_client_ids = {}
    client_ids = []
    
    ## TO ADD: BROWSING VERSION: BOUNCED, ENGAGED, PURCHASE INTENT?
    print(f"--execute_browsing_flow fired")
    # Define browser; 
    driver = browser_setup(browser, headless)

    # Mocking the Geolocation
    #driver.execute_cdp_cmd("Emulation.setGeolocationOverride", coordinates)

    # Choose a random landing page
    landing_page = get_landing_page(driver, source)
    

    # ----------> Navigation section <----------

    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Stay on the page for x seconds
    time.sleep(SHORT_TIME)

    # Give/deny consent
    consent(driver, landing_page)
    # save device_id in file to reuse later
    # Load existing cookie pairs from file, if it exists
    try:
        if os.path.exists(client_ids_file):
            with open(client_ids_file, 'r') as file:
                client_ids = json.load(file)

        if len(client_ids)<150: #limit the client_ids to 150ish in total to avoid the machine from exploding while calculating length
            temp_client_ids = save_user_id(driver)

    except Exception as e:
        print(f"Error with client_ids.json because: {e}")


    # Stay on the page for x seconds
    time.sleep(SHORT_TIME)

    #determine path
    path = random.choice(path_functions)

    if path != "bounced":
        # Choose a random category for the product
        # Example: Click on a link with the text "Example Link"
        try:
            time.sleep(SHORT_TIME)
            link = driver.find_element(By.LINK_TEXT,"Yes")
            link.click()
            print("Clicked on the link.")
            time.sleep(SHORT_TIME)
        except Exception as e:
        	print(f"An error occurred with click on link with page {landing_page}: {e}")
    else:
    	print("Bounced.")

    if path == "product" or path == "add_to_cart":
        print("product or add to cart")
        #determine product page and go to it
        
        
        category = random.choice(product_categories)
        product_id = str(random.randint(1, 3))
        driver.get(f"{base_url}{category}/{product_id}.php")
        try: 
            WebDriverWait(driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')
            print("got to product page")
        except TimeoutException:
            print("Page did not load")

        if path == "add_to_cart":
            print("add to cart branch.")        
            try:
                link = driver.find_element(By.CLASS_NAME, "cart")
                link.click()
                print("Added to cart.")
                time.sleep(SHORT_TIME)
            except Exception as e:
                print(f"An error occurred w add to cart click on {landing_page}: {e}")
    driver.quit()
    return temp_client_ids

def simulate_user(headless):
    
    # define a browser to use; using the dedicated demo_input.json file
    browser = random_choice_based_on_distribution(demo_input['browser_distribution'])
    print(f"Selected Browser: {browser}")
    # define an Acquisition source to use; using the dedicated demo_input.json file
    source = random_choice_based_on_distribution(demo_input['source_distribution'])
    print(f"Selected Source: {source}")
    
    # define path: purchase or not?
    is_purchase = random.random() < demo_input['cvr_by_source'][source]
    if is_purchase:
        temp_client_ids = execute_purchase_flow(browser, source, headless)
        return temp_client_ids
    else:
        temp_client_ids = execute_browsing_flow(browser, source, headless)
        return temp_client_ids   
     

    
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



def main():
    client_ids_file = '/Applications/MAMP/htdocs/demo_project/client_ids.json'

    # Load existing data from the file, if it exists
    if os.path.exists(client_ids_file):
        with open(client_ids_file, 'r') as file:
            try:
                all_client_ids = json.load(file)
            except json.JSONDecodeError:
                print("Error reading the existing client_ids.json file.")
                all_client_ids = []
    else:
        all_client_ids = []

    # Create a pool of processes
    with ProcessPoolExecutor(max_workers=NR_USERS) as executor:
        # Start the simulate_user processes and collect their futures
        futures = [executor.submit(simulate_user, HEADLESS) for _ in range(NR_USERS)]

        # Wait for each process to complete and collect its result
        for future in futures:
            temp_client_ids = future.result()

            # Check if temp_client_ids is not empty
            if temp_client_ids:
                # Check if the dictionary is already in the list
                if not any(temp_client_ids == existing for existing in all_client_ids):
                    all_client_ids.append(temp_client_ids)

    # Write the updated list back to the JSON file
    with open(client_ids_file, 'w') as file:
        json.dump(all_client_ids, file)
    

if __name__ == "__main__":
    start_time = time.time()
    print(f"Hello I am main and I started at {start_time}")
    os.chdir('/Users/elenanesi/Workspace/user-simulation/')
    arguments = []

    if len(sys.argv) > 1:
        HEADLESS = sys.argv[1]
        arguments.append(sys.argv[1])
    if len(sys.argv) > 2:
        NR_USERS = int(sys.argv[2])
        arguments.append(sys.argv[2])

    main()
    log_execution_time(start_time, arguments)
    
