import requests
import json
from ga4mp import GtagMP

# Your GA4 Measurement ID
MEASUREMENT_ID = 'G-1L1YW7SZFP'  # Replace with your Measurement ID
API_SECRET = '_vs5ggfmTNCe-SSAKOsfmw'  # Optional, based on your setup
hostname = "https://www.thefairycodemother.com"

def send_event(event_name, client_id, parameters):
    """ Send an event to Google Analytics 4 using the Measurement Protocol """
    url = f'https://www.google-analytics.com/mp/collect?measurement_id={MEASUREMENT_ID}&api_secret={API_SECRET}'
    event_data = {
        'client_id': '123456.123456',  # Replace with an actual client ID or user ID
        'events': [{'name': event_name, 'params': parameters}]
    }
    response = requests.post(url, data=json.dumps(event_data))
    print(f'Event sent: {event_name}, Status Code: {response.status_code}')

def simulate_user_interaction():
    client_id: '123456.123456'
    # Simulate a page view
    send_event('page_view', client_id, {'page_location': hostname+'/home', 'client_id': '123456.123456', 'script_version':'v1 - First draft'})

    # Simulate other interactions like scroll
    send_event('scroll', client_id, {'scroll_depth': '100%'})

if __name__ == '__main__':
    simulate_user_interaction()



payload = {
        "client_id": '',
        "non_personalized_ads": True,
        "events": [
            {
                "name": "try_path1",
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