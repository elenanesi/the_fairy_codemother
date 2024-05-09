from elena_util import *
app = Flask(__name__)

# --- GLOBAL VARS WITH DEFAULT VALUES ---- #

# WIP: will be used to perform a dataLayer push and keep the GA data updated with the version in use.
# SCRIPT_VERSION = "May 7"

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
product_ids = ["1","2"]
# run headless by default
HEADLESS = True
# number of users and sessions to run at every execution of the script
NR_USERS = 250
# Initializing multiple variables
BASE_URL, SHORT_TIME, LONG_TIME, page_categories, path_functions = None, 1, 5, None, None


# --- END OF GLOBAL VARS WITH DEFAULT VALUES ---- #


def get_landing_page(page, source, demo_input, process_number):
    # Setup of landing page
    utm_parameters = ""
    if (source != "direct"):
        if "organic" in source:
            utm_parameters="?utm_source=" + demo_input[source]['source'] + "&utm_medium=" + demo_input[source]['medium']
        else:
            utm_parameters="?utm_source=" + demo_input[source]['source'] + "&utm_medium=" + demo_input[source]['medium'] + "&utm_campaign=" + demo_input[source].get('campaign', '')
    print(color_text(f"-- {process_number}: Selected utms: {utm_parameters}", "green"))
    landing_page = random.choice(page_categories)  # Choosing a random page category

    # Assign a random landing page
    # product category options
    product_categories = list(products.keys())
    if landing_page == "product":
        # Choose a random category for the product
        category = random.choice(product_categories)
        # Generate a random product ID between 1 and 10
        product_id = int(random.choice(product_ids))
        product_name = ""
        for product in products.get(category, []):  # Default to empty list if category not found
            if product['item_id'] == product_id:
                product_name = product['item_name']
                break
        
        # Construct and navigate to the product URL
        url = f"{BASE_URL}{category}/{product_name}{utm_parameters}"
        print(color_text(f"-- {process_number}: Starting navigation at {url}..", "blue"))
        page.goto(url)
        return url

    elif landing_page == "category":
        # Choose a random category
        category = random.choice(product_categories)
        # Navigate to the category URL
        url = f"{BASE_URL}category/{category}{utm_parameters}"
        print(color_text(f"-- {process_number}: Starting navigation at {url}..", "blue"))
        page.goto(url)
        return url

    else:
        # Navigate to a generic page URL
        url = f"{BASE_URL}{utm_parameters}"
        print(color_text(f"-- {process_number}: Starting navigation at {url}..", "blue"))
        page.goto(url)
        return url

def execute_purchase_flow(browser_input, source, device, consent_level, demo_input, headless, process_number):

    print(color_text(f"-- {process_number}: execute_purchase_flow fired", "green")) 

    browser = browser_setup(browser_input, device, headless, process_number)
    context = browser.new_context()
    page = context.new_page()
    print(color_text(f"-- {process_number}: browser was correctly setup", "green"))

    # Setup of utms
    utm_parameters = ""
    if (source != "direct"):
        if "organic" in source:
            utm_parameters="?utm_source=" + demo_input[source]['source'] + "&utm_medium=" + demo_input[source]['medium']
        else:
            utm_parameters="?utm_source=" + demo_input[source]['source'] + "&utm_medium=" + demo_input[source]['medium'] + "&utm_campaign=" + demo_input[source].get('campaign', '')
    print(color_text(f"-- {process_number}: Selected utms: {utm_parameters}", "green"))

    # setup of landing page
    landing_page = BASE_URL + utm_parameters
    page.goto(landing_page)
    print(color_text(f"-- {process_number}: Starting navigation at {landing_page}", "green"))
    time.sleep(LONG_TIME)

    # Give/deny consent
    consent(page, process_number, landing_page, consent_level)
    time.sleep(SHORT_TIME)

    # Scroll to the bottom of the page
    page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
    print(color_text(f"-- {process_number}: product page started", "blue"))

    ## TO ADD: PURCHASE VERSION: NEW/RETURNING CLIENT, FROM BEGINNING OR FROM ADD TO CART OR OTHER?

    # Choose a random category for the product
    product_categories = list(products.keys())
    category = random.choice(product_categories)
    # Generate a random product ID between 1 and 10
    product_id = int(random.choice(product_ids))

    product_name = ""
    for product in products.get(category, []):  # Default to empty list if category not found
        if product['item_id'] == product_id:
            product_name = product['item_name']
            break

    page.goto(f"{BASE_URL}{category}/{product_name}")
    print(color_text(f"-- {process_number}: product page visited at {BASE_URL}{category}/{product_name}", "green"))
    time.sleep(SHORT_TIME)
    try: 
        page.wait_for_load_state('networkidle')
        print(color_text(f"-- {process_number}:  got to product page", "green"))
    except TimeoutException:
        print(color_text(f"-- {process_number}: Page did not load", "red"))

    print(color_text(f"-- {process_number}: add to cart started", "blue"))       
    try:
        link = page.query_selector(".cart")
        link.click()
        print(color_text(f"-- {process_number}: added to cart", "green")) 
        time.sleep(SHORT_TIME)
    except Exception as e:
        print(color_text(f"-- {process_number}: An error occurred w add to cart click on {landing_page}: {e}", "red"))

    try:
        link = page.query_selector(".your-cart") 
        link.click()
        print(color_text(f"-- {process_number}: your-cart clicked", "green")) 
        time.sleep(SHORT_TIME)
    except Exception as e:
        print(color_text(f"-- {process_number}: An error occurred w checkout: {e}", "red"))

    try:
        link = page.query_selector(".checkout")
        print(color_text(f"-- {process_number}: checkout started", "green")) 
        link.click()
        print(color_text(f"-- {process_number}: Purchase completed", "green")) 
        time.sleep(LONG_TIME)
    except Exception as e:
        print(color_text(f"-- {process_number}: An error occurred w checkout: {e}", "red"))
    

    browser.close()

def execute_browsing_flow(browser_input, source, device, consent_level, demo_input, headless, process_number):
    print(color_text(f"-- {process_number}: execute_browsing_flow fired", "green"))


    browser = browser_setup(browser_input, device, headless, process_number)
    context = browser.new_context()
    page = context.new_page()
    print(color_text(f"-- {process_number}: browser was correctly setup", "green"))

    # Mocking the Geolocation (does not work for now :( , investigating.)
    # driver.execute_cdp_cmd("Emulation.setGeolocationOverride", coordinates)

    # Choose a random landing page
    landing_page = get_landing_page(page, source, demo_input, process_number)
    print(color_text(f"-- {process_number}: Landing page was correctly setup", "green"))
    
    time.sleep(SHORT_TIME)

    # ----------> Navigation section <----------

    # Scroll to the bottom of the page
    page.evaluate("window.scrollTo(0, document.body.scrollHeight);")

    # Stay on the page for x seconds
    time.sleep(SHORT_TIME)

    # Give/deny consent
    consent(page, process_number, landing_page, consent_level)
    print(color_text(f"-- {process_number}: consent {consent_level} applied", "green"))

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
            link = page.query_selector(".next")
            link.click()
            print(color_text(f"-- {process_number}: Clicked on an internal link", "green"))
        except Exception as e:
            print(color_text(f"-- {process_number}: An error occurred with click on link with page {landing_page}: {e}", "red"))
    else:
            print(color_text(f"-- {process_number}: bounced session", "green"))

    if path == "product" or path == "add_to_cart":
        print(color_text(f"-- {process_number}: product page branch started", "blue"))
        # Choose a random category for the product
        category = random.choice(product_categories)
        # Generate a random product ID between 1 and 10
        product_id = int(random.choice(product_ids))
        product_name = ""
        for product in products.get(category, []):  # Default to empty list if category not found
            if product['item_id'] == product_id:
                product_name = product['item_name']
                break
        page.goto(f"{BASE_URL}{category}/{product_name}")
        print(color_text(f"-- {process_number}: product page visited at {BASE_URL}{category}/{product_name}", "green"))
        time.sleep(SHORT_TIME)

        try: 
            page.wait_for_load_state('networkidle')
            print(color_text(f"-- {process_number}:  got to product page", "green"))
        except TimeoutException:
            print(color_text(f"-- {process_number}: Page did not load", "red"))

        if path == "add_to_cart":
            print(color_text(f"-- {process_number}: add to cart branch started", "blue"))       
            try:
                link = page.query_selector(".cart")
                link.click()
                print(color_text(f"-- {process_number}: added to cart", "green")) 
                time.sleep(SHORT_TIME)
            except Exception as e:
                print(color_text(f"-- {process_number}: An error occurred w add to cart click on {landing_page}: {e}", "red"))
    browser.close()
    return

    def simulate_user(headless, demo_input, process_number):
        global CLIENT_IDS_PATH, BASE_URL, MAX_CLIENT_IDS, SHORT_TIME, LONG_TIME, page_categories, product_categories, path_functions, GA_MEASUREMENT_ID, CHROME_DRIVER, FIREFOX_DRIVER, ga_cookie_name
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
            product_categories = demo_input['product_categories']
            path_functions = demo_input['path_functions']
            CHROME_DRIVER = demo_input['CHROME_DRIVER']
            FIREFOX_DRIVER = demo_input['FIREFOX_DRIVER']

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
            return temp_client_id   

def simulate_user(headless, demo_input, process_number):
    global BASE_URL, SHORT_TIME, LONG_TIME, page_categories, path_functions
    # initiate global vars with values from the input file
    BASE_URL = demo_input['BASE_URL']
    SHORT_TIME = demo_input['SHORT_TIME']
    LONG_TIME = demo_input['LONG_TIME']
    page_categories = demo_input['page_categories']
    # products = demo_input['products']
    path_functions = demo_input['path_functions']

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
        execute_purchase_flow(browser, source, device, consent_level, demo_input, headless, process_number)
        return 
    else:
        print(color_text(f"---- {process_number}: Selected browsing_flow", "green"))
        execute_browsing_flow(browser, source, device, consent_level, demo_input, headless, process_number)
        return    

def main(demo_input):
    print(color_text(f"------ Launching {NR_USERS} processes, headless is {HEADLESS}", "blue"))

    # Create a pool of processes
    with ProcessPoolExecutor(max_workers=NR_USERS) as executor:
        # Start the simulate_user processes and collect their futures
        futures = [executor.submit(simulate_user, HEADLESS, demo_input, process_number) for process_number in range(NR_USERS)]

        # Wait for each process to complete
        for future in futures:
            future.result()  # Ensures each process completes; no value is expected

        print(color_text("All processes completed successfully.", "green"))


@app.route('/', defaults={'headless': 1, 'nr_users': 0})

@app.route('/<int:headless>/', defaults={'nr_users': 0})

@app.route('/<int:headless>/<int:nr_users>')
def run_script(headless, nr_users):
    global HEADLESS, NR_USERS
    process_number = 0

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

    HEADLESS = bool(headless)
    if nr_users == 0:
        print(color_text("---------- Simulate_user was called without arguments, so I will choose them", "blue"))
        # check today's day
        today = date.today()
        weekday = today.weekday()

        # is today a week day?
        if weekday < 5:
            #choose a random number of processes to run, which will be the final number of sessions/users 
            NR_USERS = random.randint(80, 100)
            print(color_text(f"-------- Weekday branch: Today is day {weekday} of the week, I am launching {NR_USERS} processes", "blue"))
        else:
            #choose a random number of processes to run, which will be the final number of sessions/users 
            NR_USERS = random.randint(150, 200)
            print(color_text(f"-------- Weekend branch: Today is day {weekday} of the week, I am launching {NR_USERS} processes", "blue"))
    else:
        NR_USERS = nr_users
    # go ahead and have fun
    response = main(demo_input)
    # let's log how long it took to execute all of this
    log_execution_time(start_time, arguments)
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)


# end of script


