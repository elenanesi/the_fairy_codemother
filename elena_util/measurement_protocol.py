import requests
import json
import random
import sys
from datetime import datetime, timedelta

from elena_util import *



# --------  Global vars. -------- #

MEASUREMENT_ID = 'G-1L1YW7SZFP'  # Replace with your Measurement ID
API_SECRET = '_vs5ggfmTNCe-SSAKOsfmw'  # Optional, based on your setup
HOSTNAME = "https://www.thefairycodemother.com"
SCRIPT_VERSION = "v12 - refined path, working on user type recognition"
CLIENT_ID = ''
client_ids = ''
engagement_time_msec = 100
client_ids_file = 'client_ids.json'

def website_visit():
    events = [{
            "name": "page_view",
            "params": {          
                        'page_location': HOSTNAME+'/home',
                        'page_title': 'thefairycodemother',
                        'script_version': SCRIPT_VERSION,
                        "session_id": "123",
                        "engagement_time_msec": engagement_time_msec,
                        "source": "google",
                        "medium": "cpc",
                        "campaign": "test"
                        }
            }
            
            ]


    return events
        
def product_view():
    category = random.choice(pages) #choosing a random page category
    events = website_visit() #events is initialized with the visit to the website

    #visit 5 random product pages after visiting the website
    i = 2
    for _ in range (2):
        i += 1
        events.append({
        "name": "page_view",
        "params": {          
                    'page_location': HOSTNAME+'/product/'+category+"/"+str(random.randint(1,10)),
                    'script_version': SCRIPT_VERSION,
                    "session_id": "123",
                    "engagement_time_msec": engagement_time_msec*i
                }
        })
        events.append({
        "name": "event_v13",
        "params": {          
                    'page_location': HOSTNAME+'/product/'+category+"/"+str(random.randint(1,10)),
                    'script_version': SCRIPT_VERSION,
                    "session_id": "123",
                    "engagement_time_msec": engagement_time_msec*i
                }
        })

    return events

path_functions = {
    'bounce' : website_visit,
    'engaged': product_view
}

pages = ["apples", "oranges", "grapes"]

# List of user-agent strings for different browsers and devices
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (Linux; Android 9; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Mobile Safari/537.36',
    # Add more user agents as needed
]

# --------  END Global vars. -------- # 

def log_message():
    with open("logfile.log", "a") as log_file:
        log_file.write(f"Function called at {datetime.now()}\n")

def send_past_event():
    url = f'https://www.google-analytics.com/mp/collect?measurement_id={MEASUREMENT_ID}&api_secret={API_SECRET}'
    # Get the current date and time
    current_time = datetime.now()
    # Subtract 7 days
    time_seven_days_ago = current_time - timedelta(days=1)
    # Format as a timestamp, for example, in the format "YYYY-MM-DD HH:MM:SS"
    timestamp = int(time_seven_days_ago.timestamp() * 1000)
    print(timestamp)

    payload = {
        "client_id": '',
        "timestamp_micros":timestamp,
        "events": [
            {
                "name": "test_elena_timestamp",
                "params": {          
                'page_location': HOSTNAME+'/home',
                'script_version': SCRIPT_VERSION,
                "campaign_id": "google_1234",
                "campaign": "Summer_fun",
                "source": "google",
                "medium": "cpc",
                "term": "summer+travel",
                "content": "logolink",
                "session_id": "123",
                "engagement_time_msec": "100"
                }
            }
            ]
    }

    for _ in range(2):  
        # Simulate for up to 5 users
        # Generate a client ID in GA format
        payload['client_id'] = generate_client_id(client_ids_file, client_ids)
        #print(f'Payload: {payload}')
      
        # Select a random user agent
        #parameters['user_agent'] = random.choice(user_agents)


        r = requests.post(url,data=json.dumps(payload),verify=True)
        print(r.status_code)

def send_event(path):
    # set request
    url = f'https://www.google-analytics.com/mp/collect?measurement_id={MEASUREMENT_ID}&api_secret={API_SECRET}'
    #url = f'https://www.google-analytics.com/debug/mp/collect?measurement_id={MEASUREMENT_ID}&api_secret={API_SECRET}'
    
    # desperately trying different options to integrate consent
    # "consent": {'analytics_storage':'granted', 'ad_storage':'denied', 'ad_user_data':'denied', 'ad_personalization':'denied'},
    # "non_personalized_ads":1,  ,

    #get sequence of events based on chosen path
    path_function = path_functions.get(path)
    if path_function:
        events = path_function()
    else:
        print(f"Invalid path selected: {path}")
        return


    
    l = len(events)

    payload = {
        "client_id": '',
        "non_personalized_ads": True,
        "events": events
    }

    # Simulate for up to x users

    for _ in range(2):  
        # Generate a client ID in GA format
        client_id = generate_client_id(client_ids_file, client_ids)

        payload['client_id'] = client_id
        #Generate a session ID
        session_id = random.randint(100, 999)
        i = 0
        for item in events:
            #set session_id for each event in the array
            payload['events'][i]['params']['session_id'] = session_id
            i += 1
            print(f'session: {session_id}')
      
        # Select a random user agent
        #parameters['user_agent'] = random.choice(user_agents)

        #send the events for this user
        r = requests.post(url,data=json.dumps(payload),verify=True)
        print(r.status_code, client_id, client_ids.get(client_id))


    

if __name__ == '__main__':
    # Change the current working directory
    os.chdir('/Users/elenanesi/user-simulation/')
    log_message()
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        client_ids_file = sys.argv[2] if len(sys.argv) > 2 else 'client_ids.json'
        client_ids = get_client_ids(client_ids_file)
        send_event(input_path)
    else:
        print("No path argument provided. Please specify a valid path (e.g., 'path_1').")
