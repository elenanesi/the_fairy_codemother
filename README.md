# demo_dataset
automation to create a GA4 demo data set 

To make this script work, you'll need to have 

1) A localhost website to navigate. 
The script expects a link with text "Yes" in all pages; An "Add to cart" button on product pages, and a "Purchase" link in the checkout page

2) browser drivers installed on the machine.
The location of the drivers is defined in the global vars of the file simulate_users_chrome.py
CHROME_DRIVER

3) global vars to initiate: browser drivers and base url for navigation
