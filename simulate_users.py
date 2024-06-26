from elena_util import *


# --- GLOBAL VARS WITH DEFAULT VALUES ---- #

# WIP: will be used to perform a dataLayer push and keep the GA data updated with the version in use.
# SCRIPT_VERSION = "April 19"

# default max number of client ids allowed in the client ids file
MAX_CLIENT_IDS = 500
# default intervals of seconds used for time.sleep within the code (make them shorter if you want the script to go faster)
SHORT_TIME = 5
LONG_TIME = 7
# page category options
page_categories = ["home", "category", "product"]

# Product "feed"
# to be substituted with JSON/Other file to be shared w the Flask website
products = {
    'electronics': [
        {'item_id': 1, 'item_name': 'Laptop', 'item_category': 'electronics', 'price': 800, 'quantity': 0, 'description': 'High-performance laptop.', 'image': 'url_to_image'},
        {'item_id': 2, 'item_name': 'Smartphone', 'item_category': 'electronics', 'price': 500, 'quantity': 0, 'description': 'Latest model smartphone.', 'image': 'url_to_image'},
    ],
    'clothing': [
        {'item_id': 1, 'item_name': 'T-Shirt', 'item_category': 'clothing', 'price': 20, 'quantity': 0, 'description': 'Cotton t-shirt.', 'image': 'url_to_image'},
        {'item_id': 2, 'item_name': 'Jeans', 'item_category': 'clothing', 'price': 40, 'quantity': 0, 'description': 'Denim jeans.', 'image': 'url_to_image'},
    ]
}


# product ids range options
product_ids = [1,2]

# path options
path_functions = ["bounce","engaged", "product", "add_to_cart"]
# run headless by default
HEADLESS = 1
# number of users and sessions to run at every execution of the script
NR_USERS = 250
# helper var to hold demo_input.json content
demo_input = {}
ga_cookie_name = ""

# --- END OF GLOBAL VARS WITH DEFAULT VALUES ---- #


def get_landing_page(driver, source, demo_input, process_number):
    # Setup of landing page
    utm_parameters = ""
    if (source != "direct"):
        if "organic" in source:
            utm_parameters="?utm_source=" + demo_input[source]['source'] + "&utm_medium=" + demo_input[source]['medium']
        else:
            utm_parameters="?utm_source=" + demo_input[source]['source'] + "&utm_medium=" + demo_input[source]['medium'] + "&utm_campaign=" + demo_input[source].get('campaign', '')
    print(color_text(f"-- {process_number}: Selected utms: {utm_parameters}", "green"))
    page = random.choice(page_categories)  # Choosing a random page category
    

    # Assign a random landing page
    # product category options
    product_categories = list(products.keys())
    if page == "product":
        # Choose a random category for the product
        category = random.choice(product_categories)
        # Generate a random product ID between 1 and 10
        product_id = random.choice(product_ids)
        product_name = ""
        for product in products.get(category, []):  # Default to empty list if category not found
            if product['item_id'] == product_id:
                product_name = product['item_name']
        
        # Construct and navigate to the product URL
        url = f"{BASE_URL}{category}/{product_name}{utm_parameters}"
        driver.get(url)
        return url

    elif page == "category":
        # Choose a random category
        category = random.choice(product_categories)
        # Navigate to the category URL
        url = f"{BASE_URL}category/{category}{utm_parameters}"
        driver.get(url)
        return url

    else:
        # Navigate to a generic page URL
        url = f"{BASE_URL}{utm_parameters}"
        driver.get(url)
        return url

def execute_purchase_flow(browser, source, device, consent_level, demo_input, headless, process_number):
    # vars
    temp_client_id = {}
    client_ids = []
    global HEADLESS
    # product category options
    product_categories = list(products.keys())

	## TO ADD: PURCHASE VERSION: NEW/RETURNING CLIENT, FROM BEGINNING OR FROM ADD TO CART OR OTHER?
    print(color_text(f"-- {process_number}: execute_purchase_flow fired", "green")) 

    # Setup browser; 
    driver = browser_setup(browser, device, headless, process_number)

    # Setup of utms
    utm_parameters = ""
    if (source != "direct"):
        if "organic" in source:
            utm_parameters="?utm_source=" + demo_input[source]['source'] + "&utm_medium=" + demo_input[source]['medium']
        else:
            utm_parameters="?utm_source=" + demo_input[source]['source'] + "&utm_medium=" + demo_input[source]['medium'] + "&utm_campaign=" + demo_input[source].get('campaign', '')
    print(color_text(f"-- {process_number}: Selected utms: {utm_parameters}", "green"))

    
    # Add navigation actions here

    # url is landing page
    url = BASE_URL + utm_parameters
    driver.get(url)  # Your website URL

    # Give/deny consent
    consent(driver, url, consent_level)
    # save device_id in file to reuse later for returning users simulation
    try:
        if os.path.exists(CLIENT_IDS_PATH):
            with open(CLIENT_IDS_PATH, 'r') as file:
                client_ids = json.load(file)
        else:
            client_ids = []

        if len(client_ids)<MAX_CLIENT_IDS: #limit the client_ids to avoid the machine from exploding while calculating length
            temp_client_id = save_client_id(driver, ga_cookie_name)

    except Exception as e:
        print(color_text(f"-- {process_number}: Error with client_ids.json because: {e}", "red")) 

    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print(color_text(f"-- {process_number}: product page started", "blue"))
    # Choose a random category for the product
    category = random.choice(product_categories)
    # Generate a random product ID between 1 and 10
    product_id = random.choice(product_ids)
    product_name = ""
    for product in products.get(category, []):  # Default to empty list if category not found
        if product['item_id'] == product_id:
            product_name = product['item_name']

    driver.get(f"{BASE_URL}{category}/{product_name}")
    try: 
        WebDriverWait(driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        print(color_text(f"-- {process_number}:  got to product page", "green"))
    except TimeoutException:
        print(color_text(f"-- {process_number}: Page did not load", "red"))

    print(color_text(f"-- {process_number}: add to cart started", "blue"))       
    try:
        link = driver.find_element(By.CLASS_NAME, "cart")
        link.click()
        print(color_text(f"-- {process_number}: added to cart", "green")) 
        time.sleep(SHORT_TIME)
    except Exception as e:
        print(color_text(f"-- {process_number}: An error occurred w add to cart click on {landing_page}: {e}", "red"))

    try:
        link = driver.find_element(By.CLASS_NAME, "your-cart")
        link.click()
        print(color_text(f"-- {process_number}: your-cart clicked", "green")) 
        time.sleep(SHORT_TIME)
    except Exception as e:
        print(color_text(f"-- {process_number}: An error occurred w checkout: {e}", "red"))

    try:
        link = driver.find_element(By.CLASS_NAME, "checkout")
        print(color_text(f"-- {process_number}: checkout started", "green")) 
        link.click()
        print(color_text(f"-- {process_number}: Purchase completed", "green")) 
        time.sleep(LONG_TIME)
    except Exception as e:
        print(color_text(f"-- {process_number}: An error occurred w checkout: {e}", "red"))
    

    driver.quit()

def execute_browsing_flow(browser, source, device, consent_level, demo_input, headless, process_number):
    print(color_text(f"-- {process_number}: execute_browsing_flow fired", "green"))

    # vars to save the client_id generated (if any)
    temp_client_id = {}
    client_ids = []

    # Setup browser; 
    driver = browser_setup(browser, device, headless, process_number)
    print(color_text(f"-- {process_number}: browser was correctly setup", "green"))

    # Mocking the Geolocation (does not work for now :( , investigating.)
    # driver.execute_cdp_cmd("Emulation.setGeolocationOverride", coordinates)

    # Choose a random landing page
    landing_page = get_landing_page(driver, source, demo_input, process_number)
    print(color_text(f"-- {process_number}: Landing page was correctly setup", "green"))
    print(color_text(f"-- {process_number}: Starting navigation at {landing_page}..", "blue"))

    # ----------> Navigation section <----------

    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Stay on the page for x seconds
    time.sleep(SHORT_TIME)

    # Give/deny consent
    consent(driver, landing_page, consent_level)
    print(color_text(f"-- {process_number}: consent {consent_level} applied", "green"))
    # save device_id in file to reuse later
    # Load existing cookie pairs from file, if it exists
    try:
        if os.path.exists(CLIENT_IDS_PATH):
            with open(CLIENT_IDS_PATH, 'r') as file:
                client_ids = json.load(file)
        else:
            client_ids = []

        if len(client_ids)<150: #limit the client_ids to 150ish in total to avoid the machine from exploding while calculating length
            temp_client_id = save_client_id(driver, ga_cookie_name)

    except Exception as e:
        print(color_text(f"-- {process_number}: Error with client_ids.json because: {e}", "red"))


    # Stay on the page for x seconds
    time.sleep(SHORT_TIME)

    #determine path
    path = random.choice(path_functions)
    # product category options
    product_categories = list(products.keys())

    if path != "bounced":
        # Choose a random category for the product
        # Example: Click on a link with the text "Example Link"
        try:
            time.sleep(SHORT_TIME)
            link = driver.find_element(By.CLASS_NAME, "next")
            link.click()
            print(color_text(f"-- {process_number}: Clicked on an internal link", "green"))
            time.sleep(SHORT_TIME)
        except Exception as e:
            print(color_text(f"-- {process_number}: An error occurred with click on link with page {landing_page}: {e}", "red"))
    else:
    	    print(color_text(f"-- {process_number}: bounced session", "green"))

    if path == "product" or path == "add_to_cart":
        print(color_text(f"-- {process_number}: product page branch started", "blue"))
        #determine product page and go to it
        category = random.choice(product_categories)
        product_id = random.choice(product_ids)
        # Choose a random category for the product
        category = random.choice(product_categories)
        # Generate a random product ID between 1 and 10
        product_id = random.choice(product_ids)
        product_name = ""
        for product in products.get(category, []):  # Default to empty list if category not found
            if product['item_id'] == product_id:
                product_name = product['item_name']
        driver.get(f"{BASE_URL}{category}/{product_name}")
        try: 
            WebDriverWait(driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')
            print(color_text(f"-- {process_number}:  got to product page", "green"))
        except TimeoutException:
            print(color_text(f"-- {process_number}: Page did not load", "red"))

        if path == "add_to_cart":
            print(color_text(f"-- {process_number}: add to cart branch started", "blue"))       
            try:
                link = driver.find_element(By.CLASS_NAME, "cart")
                link.click()
                print(color_text(f"-- {process_number}: added to cart", "green")) 
                time.sleep(SHORT_TIME)
            except Exception as e:
                print(color_text(f"-- {process_number}: An error occurred w add to cart click on {landing_page}: {e}", "red"))
    driver.quit()
    return temp_client_id

def simulate_user(headless, demo_input, process_number):
    global CLIENT_IDS_PATH, BASE_URL, MAX_CLIENT_IDS, SHORT_TIME, LONG_TIME, page_categories, path_functions, GA_MEASUREMENT_ID, SCRIPT_PATH, ga_cookie_name
    # Load demo_input.json
    with open("demo_input.json", 'r') as file:
        demo_input = json.load(file)

        # initiate global vars with values from the input file
        BASE_URL = demo_input['BASE_URL']
        MAX_CLIENT_IDS = demo_input['MAX_CLIENT_IDS']
        SHORT_TIME = demo_input['SHORT_TIME']
        LONG_TIME = demo_input['LONG_TIME']
        CLIENT_IDS_PATH = demo_input['CLIENT_IDS_PATH']
        page_categories = demo_input['page_categories']
        # products = demo_input['products']
        path_functions = demo_input['path_functions']
        GA_MEASUREMENT_ID = demo_input['GA_MEASUREMENT_ID']
        SCRIPT_PATH = demo_input['SCRIPT_PATH']
        ga_cookie_name = "_ga_"+GA_MEASUREMENT_ID

    # select randomically the dimensions based on content of demo_input, 
    # and launch either browsing_flow or execution flow based on the CVR associated with the source selected 
    # (also contained in the demo json file)
    print(color_text(f"---- {process_number}: Selecting dimensions...", "blue"))
    # define a browser to use; using the dedicated demo_input.json file
    browser = random_choice_based_on_distribution(demo_input['browser_distribution'])
    print(color_text(f"---- {process_number}: Selected Browser: {browser}", "green"))
    device = random_choice_based_on_distribution(demo_input['device_distribution'])
    print(color_text(f"---- {process_number}: Selected Device: {device}", "green"))
    # define an Acquisition source to use; using the dedicated demo_input.json file
    source = random_choice_based_on_distribution(demo_input['source_distribution'])
    print(color_text(f"---- {process_number}: Selected Source: {source}", "green"))
    # define consent level for identification/cookies
    consent_level = random_choice_based_on_distribution(demo_input['consent_distribution'])
    print(color_text(f"---- {process_number}: Selected Consent level: {consent_level}", "green"))
    # define path: purchase or not?
    is_purchase = random.random() < demo_input['cvr_by_source'][source]
    if is_purchase:
        print(color_text(f"---- {process_number}: Selected purchase_flow", "green"))
        temp_client_id = execute_purchase_flow(browser, source, device, consent_level, demo_input, headless, process_number)
        return temp_client_id
    else:
        print(color_text(f"---- {process_number}: Selected browsing_flow", "green"))
        temp_client_id = execute_browsing_flow(browser, source, device, consent_level, demo_input, headless, process_number)
        # print(f"temp_client_id: {temp_client_id}")
        return temp_client_id   

def main():
    print(color_text(f"------ Launching {NR_USERS} processes", "blue"))
    # create an empty array to collect the client_ids produced by the processes we are going to launch
    all_client_ids = []
    global process_number
    # Load existing data from the file, if it exists
    if os.path.exists(CLIENT_IDS_PATH):
        with open(CLIENT_IDS_PATH, 'r') as file:
            try:
                all_client_ids = json.load(file)
            except json.JSONDecodeError:
                all_client_ids = []
                print(color_text("------ Error reading the existing client_ids.json file.", "red"))

    # Create a pool of processes
    with ProcessPoolExecutor(max_workers=NR_USERS) as executor:
        # Start the simulate_user processes and collect their futures

        futures = [executor.submit(simulate_user, HEADLESS, demo_input, process_number) for process_number in range(NR_USERS)]

        # Wait for each process to complete and collect its result
        for future in futures:
            # save the result (client_id) in temp_client_id, to be merged with all_client_ids
            temp_client_id = future.result()
            # print(f"temp_client_id: {temp_client_id}")

            # Check if temp_client_id is not empty
            if temp_client_id:
                # Check if the client_id is already in the list (we don't want duplicates in the file!)
                if not any(temp_client_id == existing for existing in all_client_ids):
                    all_client_ids.append(temp_client_id)

    # Now all processes have provided their temp_client_id: you can write the updated list back to the JSON file
    if all_client_ids:
        # print(f"all_client_ids: {all_client_ids}")
        with open(CLIENT_IDS_PATH, 'w') as file:
            json.dump(all_client_ids, file) 

if __name__ == "__main__":
    process_number = 0

    try:

        # checking start time so that I can log how long the script takes to execute
        start_time = time.time()

        print(color_text("---------- Welcome to simulate_users!", "green"))

        # Check if demo_input.json exists and scold user if it's not there
        if not os.path.exists("demo_input.json"):
            print(color_text("------ Are you KIDDING ME? demo_input.json is missing!!", "red"))
            time.sleep(1)
            print(color_text("------ Put it back RIGHT NOW!", "red"))
            time.sleep(1)
            sys.exit(color_text("------ I'm not sure you deserve to win the Golden punchcard.\n------ I'm going to the SPA and I am taking Zoli with me. BYE.", "red"))

        with open("demo_input.json", 'r') as file:
            demo_input = json.load(file)

            # initiate global vars with values from the input file
            BASE_URL = demo_input['BASE_URL']
            MAX_CLIENT_IDS = demo_input['MAX_CLIENT_IDS']
            SHORT_TIME = demo_input['SHORT_TIME']
            LONG_TIME = demo_input['LONG_TIME']
            CLIENT_IDS_PATH = demo_input['CLIENT_IDS_PATH']
            page_categories = demo_input['page_categories']
            # products = demo_input['products']
            path_functions = demo_input['path_functions']
            GA_MEASUREMENT_ID = demo_input['GA_MEASUREMENT_ID']
            SCRIPT_PATH = demo_input['SCRIPT_PATH']
            SHORT_TIME = demo_input['SHORT_TIME']
            LONG_TIME = demo_input['LONG_TIME']
            ga_cookie_name = "_ga_"+GA_MEASUREMENT_ID

        # define a var for the arguments
        arguments = []

        # are there input arguments?
        # no arguments:
        if len(sys.argv) <= 1:
            print(color_text("---------- Simulate_user was called without arguments, so I will choose them", "blue"))
            # check today's day
            today = date.today()
            weekday = today.weekday()

            # is today a week day?
            if weekday < 5:
                #choose a random number of processes to run, which will be the final number of sessions/users 
                NR_USERS = random.randint(80, 100)
                print(color_text(f"-------- Weeday branch: Today is day {weekday} of the week, I am launching {NR_USERS} processes", "blue"))
            else:
                #choose a random number of processes to run, which will be the final number of sessions/users 
                NR_USERS = random.randint(150, 200)
                print(color_text(f"-------- Weekend branch: Today is day {weekday} of the week, I am launching {NR_USERS} processes", "blue"))

        # script has been called w arguments:
        if len(sys.argv) > 1:
            HEADLESS = sys.argv[1]
            arguments.append(sys.argv[1])
        if len(sys.argv) > 2:
            NR_USERS = int(sys.argv[2])
            arguments.append(sys.argv[2])

        # go ahead and have fun
        main()
        # let's log how long it took to execute all of this
        log_execution_time(start_time, arguments)
    except Exception as e:
        # Get current traceback object
        tb = traceback.extract_tb(e.__traceback__)
        # Get the last traceback object as it will point to the line where the error occurred
        last_tb = tb[-1]       
        # Extract filename, line number, function name, and text from the last traceback
        line_no = last_tb.lineno
        filename = last_tb.filename
        func_name = last_tb.name
        print(color_text(f"---------- {process_number} Ops, you fracked up here: {e} \n ---------- File: {filename}\n ---------- Function: {func_name}\n ---------- at line: {line_no}", "red"))
        # let's log how long it took to execute all of this
        log_execution_time(start_time, arguments)

# end of script



    
