from elena_util import *

# --- GLOBAL VARS WITH DEFAULT VALUES ---- #

# WIP: will be used to perform a dataLayer push and keep the GA data updated with the version in use.
# SCRIPT_VERSION = "May 14 - working w google cloud"

# run headless by default
HEADLESS = True
# number of users and sessions to run at every execution of the script
NR_USERS = 50
# Initializing multiple variables
BASE_URL, SHORT_TIME, LONG_TIME, page_categories, path_functions = None, 1, 5, None, None


# --- END OF GLOBAL VARS WITH DEFAULT VALUES ---- #

def get_random_page (sitemap_url):
    # Fetch the sitemap
    response = requests.get(sitemap_url)
    response.raise_for_status()  # Check if the request was successful

    # Parse the XML
    root = ET.fromstring(response.content)

    # Extract all URLs from the sitemap
    urls = [element.text for element in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]

    if not urls:
        print(color_text("No URLs found in the sitemap.", "red"))
        return None
    
    # Select a random URL
    random_url = random.choice(urls)
    return random_url

def get_landing_page(source, demo_input, process_number):
    # Define utm parameters to simulate acquisition source
    utm_parameters = ""
    if (source != "direct"):
        if "organic" in source:
            utm_parameters="utm_source=" + demo_input[source]['source'] + "&utm_medium=" + demo_input[source]['medium']
        else:
            # using get to provide a default empty value if campaign is not present
            utm_parameters="utm_source=" + demo_input[source]['source'] + "&utm_medium=" + demo_input[source]['medium'] + "&utm_campaign=" + demo_input[source].get('campaign', '')
    # print(color_text(f"-- {process_number}: Selected utms: {utm_parameters}", "green"))
    
    # Assign a random landing page
    # Choosing a random page category
    landing_page_category = random.choice(demo_input["page_categories"]) 
    if landing_page_category == "home":
        landing_page = f"{BASE_URL}/"
    else:
        sitemap_url = demo_input[f"{landing_page_category}_sitemap"]
        landing_page =  get_random_page(sitemap_url) 
    if utm_parameters:
        landing_page += f"?{utm_parameters}"

    return landing_page

def execute_purchase_flow(browser_input, source, device, consent_level, demo_input, headless, process_number):

    print(color_text(f"-- {process_number}: execute_purchase_flow fired", "green")) 

    # setup browser and context
    browser, context = browser_setup(browser_input, device, headless, process_number)
    #context.set_javascript_enabled(True)

    # setup browser page
    page = context.new_page()
    print(color_text(f"-- {process_number}: browser was correctly setup", "green"))

    # Setup of utms
    utm_parameters = ""
    if (source != "direct"):
        if "organic" in source:
            utm_parameters="utm_source=" + demo_input[source]['source'] + "&utm_medium=" + demo_input[source]['medium']
        else:
            utm_parameters="utm_source=" + demo_input[source]['source'] + "&utm_medium=" + demo_input[source]['medium'] + "&utm_campaign=" + demo_input[source].get('campaign', '')
    print(color_text(f"-- {process_number}: Selected utms: {utm_parameters}", "green"))

    # setup of landing page
    landing_page = f"{BASE_URL}?{utm_parameters}"
    page.goto(landing_page)
    print(color_text(f"-- {process_number}: Starting navigation at {landing_page}", "green"))
    time.sleep(LONG_TIME)

    # Scroll to the bottom of the page
    page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
    print(color_text(f"-- {process_number}: product page started", "blue"))

    # Give/deny consent
    consent(page, process_number, landing_page, consent_level)
    time.sleep(SHORT_TIME)

    ## TO ADD: PURCHASE VERSION: NEW/RETURNING CLIENT, FROM BEGINNING OR FROM ADD TO CART OR OTHER?

    # go to product page
    url = get_random_page(demo_input["product_sitemap"])
    page.goto(url)
    print(color_text(f"-- {process_number}: product page branch started at {url}", "blue"))
    time.sleep(SHORT_TIME)

    try: 
        page.wait_for_load_state('networkidle')
    except TimeoutException:
        print(color_text(f"-- {process_number}: Page did not load", "red"))

    print(color_text(f"-- {process_number}: add to cart started", "blue"))       
    try:
        link = page.query_selector(demo_input["add_to_cart_selector"])
        link.click()
        print(color_text(f"-- {process_number}: added to cart", "green")) 
        time.sleep(SHORT_TIME)
    except Exception as e:
        print(color_text(f"-- {process_number}: An error occurred w add to cart click on {landing_page}: {e}", "red"))

    try:
        link = page.query_selector(demo_input["cart_selector"]) 
        link.click()
        print(color_text(f"-- {process_number}: your-cart clicked", "green")) 
        time.sleep(SHORT_TIME)
    except Exception as e:
        print(color_text(f"-- {process_number}: An error occurred w checkout: {e}", "red"))

    try:
        link = page.query_selector(demo_input["checkout_selector"])
        print(color_text(f"-- {process_number}: checkout started", "green")) 
        link.click()
        print(color_text(f"-- {process_number}: Purchase completed", "green")) 
        time.sleep(LONG_TIME)
    except Exception as e:
        print(color_text(f"-- {process_number}: An error occurred w checkout: {e}", "red"))
    
    context.close()
    browser.close()

def execute_browsing_flow(browser_input, source, device, consent_level, demo_input, headless, process_number):
    print(color_text(f"-- {process_number}: execute_browsing_flow fired", "green"))

    browser, context = browser_setup(browser_input, device, headless, process_number)
    page = context.new_page()

    # Choose a random landing page
    landing_page = get_landing_page(source, demo_input, process_number)
    print(color_text(f"-- {process_number}: Landing page was correctly setup, visiting {landing_page}", "green"))
    page.goto(landing_page)
    
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

    if path != "bounced":
        # Choose a random category for the product
        # Example: Click on a link with the text "Example Link"
        try:
            time.sleep(SHORT_TIME)
            link = page.query_selector(demo_input["first_click_selector"])
            link.click()
            print(color_text(f"-- {process_number}: Clicked on an internal link", "green"))
        except Exception as e:
            print(color_text(f"-- {process_number}: An error occurred with click on link with page {landing_page}: {e}", "red"))
    else:
            print(color_text(f"-- {process_number}: bounced session", "green"))

    if path == "product" or path == "add_to_cart":
        print(color_text(f"-- {process_number}: product page branch started", "blue"))
        url = get_random_page(demo_input["product_sitemap"])
        page.goto(url)
        print(color_text(f"-- {process_number}: product page branch started at {url}", "blue"))
        time.sleep(SHORT_TIME)

        try: 
            page.wait_for_load_state('networkidle')
        except TimeoutException:
            print(color_text(f"-- {process_number}: Page did not load", "red"))

        if path == "add_to_cart":
            print(color_text(f"-- {process_number}: add to cart branch started", "blue"))       
            try:
                link = page.query_selector(demo_input["add_to_cart_selector"])
                link.click()
                print(color_text(f"-- {process_number}: added to cart", "green")) 
                time.sleep(SHORT_TIME)
            except Exception as e:
                print(color_text(f"-- {process_number}: An error occurred w add to cart click on {landing_page}: {e}", "red"))
    context.close()
    browser.close()
    return

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
        futures = [executor.submit(simulate_user, bool(int(HEADLESS)), demo_input, process_number) for process_number in range(NR_USERS)]

        # Wait for each process to complete
        for future in futures:
            future.result()  # Ensures each process completes; no value is expected

        print(color_text("All processes completed successfully.", "green"))


if __name__ == "__main__":
    process_number = 0
    #Track CO2 improvements over time with the CodeCarbon PY lib
    tracker = EmissionsTracker()
    tracker.start()

    # checking start time so that I can log how long the script takes to execute
    start_time = time.time()

    print(color_text("---------- Welcome to simulate_users!", "green"))


    # aux var to hold demo_input.json content
    demo_input = {}

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
        SHORT_TIME = demo_input['SHORT_TIME']
        LONG_TIME = demo_input['LONG_TIME']
        page_categories = demo_input['page_categories']
        # products = demo_input['products']
        path_functions = demo_input['path_functions']

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
            NR_USERS = random.randint(20, 40)
            print(color_text(f"-------- Weeday branch: Today is day {weekday} of the week, I am launching {NR_USERS} processes", "blue"))
        else:
            #choose a random number of processes to run, which will be the final number of sessions/users 
            NR_USERS = random.randint(50, 70)
            print(color_text(f"-------- Weekend branch: Today is day {weekday} of the week, I am launching {NR_USERS} processes", "blue"))

    # script has been called w arguments:
    if len(sys.argv) > 1:
        HEADLESS = sys.argv[1]
        arguments.append(sys.argv[1])
    if len(sys.argv) > 2:
        NR_USERS = int(sys.argv[2])
        arguments.append(sys.argv[2])

    # go ahead and have fun
    main(demo_input)
    # let's log how long it took to execute all of this
    log_execution_time(start_time, arguments)
    tracker.stop()

# end of script
