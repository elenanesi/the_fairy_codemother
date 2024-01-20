import requests
import json
import random
import sys
from datetime import datetime, timedelta
from .client_id_utils import generate_client_id

def website_visit(HOSTNAME, SCRIPT_VERSION, engagement_time_msec, pages):
    events = []
    events.append({
        "name": "website_visit",
        "params": {          
                    'page_location': HOSTNAME+'/home',
                    'script_version': SCRIPT_VERSION,
                    "session_id": "123",
                    "engagement_time_msec": engagement_time_msec
                }
        })

    i = 1
    for _ in range (2):
        i += 1
        events.append({
        "name": "website_visit",
        "params": {          
                    'page_location': HOSTNAME+'/'+ random.choice(pages),
                    'script_version': SCRIPT_VERSION,
                    "session_id": "123",
                    "engagement_time_msec": engagement_time_msec*i
                }
        })

    return events
        
def product_view(HOSTNAME, SCRIPT_VERSION, engagement_time_msec, category):
    category = random.choice(pages) #choosing a random page category
    events = website_visit() #events is initialized with the visit to the website

    #visit 5 random product pages after visiting the website
    i = 2
    for _ in range (5):
        i += 1
        events.append({
        "name": "product_view",
        "params": {          
                    'page_location': HOSTNAME+'/product/'+category+"/"+str(random.randint(1,10)),
                    'script_version': SCRIPT_VERSION,
                    "session_id": "123",
                    "engagement_time_msec": engagement_time_msec*i
                }
        })

    return events