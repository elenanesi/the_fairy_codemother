from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from multiprocessing import Process
import time
import random
import sched

from elena_util import *

# get info from demo_input.json file to get the necessary input for paths
os.chdir('/Users/elenanesi/Workspace/user-simulation/')
if os.path.exists("demo_input.json"):
	with open("demo_input.json", 'r') as file:
		demo_input = json.load(file)

def random_choice_based_on_distribution(distribution_dict):
    """
    Selects an item based on a distribution of probabilities.

    :param distribution_dict: A dictionary where keys are items to choose from and values are their corresponding probabilities.
    :return: A randomly selected key based on the distribution.
    """
    items = list(distribution_dict.keys())
    weights = list(distribution_dict.values())
    return random.choices(items, weights=weights, k=1)[0]

def execute_purchase_flow(browser, source):
    print(f"execute_purchase_flow")
    options = ChromeOptions()
    service = ChromeService(executable_path='/Users/elenanesi/Desktop/Workspace/web-drivers/chromedriver')  # Update the path
    driver = webdriver.Chrome(service=service, options=options)
    utm_parameters = "?utm_source=" + demo_input[source]['source'] + "&utm_medium=" + demo_input[source]['medium'] + "&utm_campaign=" + demo_input[source].get('campaign', '')
    driver.get("http://www.thefairycodemother.com/demo_project/page_3.php" + utm_parameters)  # Your website URL
    # Add navigation actions here
    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Stay on the page for 10 seconds
    time.sleep(10)
    # Retrieve "_ga" cookie value
    ga_cookie = driver.get_cookie("_ga")
    if ga_cookie:
        ga_value = ga_cookie['value']
        # Load existing client IDs from file, if it exists
        client_ids_file = 'client_ids.json'
        if os.path.exists(client_ids_file):
            with open(client_ids_file, 'r') as file:
                client_ids = json.load(file)
        else:
            client_ids = []

        # Add the new client ID
        client_ids.append(ga_value)

        # Save the updated list to the file
        with open(client_ids_file, 'w') as file:
            json.dump(client_ids, file)
    driver.quit()

def execute_browsing_flow(browser, source):
    print(f"execute_browsing_flow fired")
    #define browser; fixed for now
    options = ChromeOptions()
    service = ChromeService(executable_path='/Users/elenanesi/Desktop/Workspace/web-drivers/chromedriver')  # Update the path
    driver = webdriver.Chrome(service=service, options=options)
    utm_parameters = "?utm_source=" + demo_input[source]['source'] + "&utm_medium=" + demo_input[source]['medium'] + "&utm_campaign=" + demo_input[source].get('campaign', '')
    print(f"Selected utms: {utm_parameters}")
    driver.get("http://www.thefairycodemother.com/demo_project/page_3.php" + utm_parameters)  # Your website URL
    
    # Add navigation actions here
    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Stay on the page for 10 seconds
    time.sleep(10)
    # Retrieve "_ga" cookie value
    ga_cookie = driver.get_cookie("_ga")
    if ga_cookie:
        ga_value = ga_cookie['value']
        # Load existing client IDs from file, if it exists
        client_ids_file = 'client_ids.json'
        if os.path.exists(client_ids_file):
            with open(client_ids_file, 'r') as file:
                client_ids = json.load(file)
                print(f"client_ids: {client_ids}")
        else:
            client_ids = []

        # Add the new client ID
        client_ids.append(ga_value)

        # Save the updated list to the file
        with open(client_ids_file, 'w') as file:
            json.dump(client_ids, file)
    driver.quit()

def simulate_user():
    
    # define a browser to use; using the dedicated demo_input.json file
    browser = random_choice_based_on_distribution(demo_input['browser_distribution'])
    print(f"Selected Browser: {browser}")
    # define an Acquisition source to use; using the dedicated demo_input.json file
    source = random_choice_based_on_distribution(demo_input['source_distribution'])
    print(f"Selected Source: {source}")
    # define path: purchase or not?
    #is_purchase = random.random() < demo_input['ctr_by_source'][source]
    #if is_purchase:
    #    execute_purchase_flow(browser, source)
    #else:
    #    execute_browsing_flow(browser, source)
    execute_browsing_flow(browser, source)	

def main():
    # List to hold all the Process objects, needed to support multiple fake users visiting at once
    processes = []

    # Create and start a separate process for each user
    for i in range(5):  # Change this number to the number of users you want to simulate
        p = Process(target=simulate_user) #target the simulate_user function
        p.start()
        processes.append(p)

    # Wait for all processes to finish
    for p in processes:
        p.join()

if __name__ == "__main__":
    main()
