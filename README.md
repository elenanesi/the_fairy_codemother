# demo_dataset
automation to create a GA4 demo data set 

INSTALLATION

To make this script work, you'll need to have 

1) A localhost website to navigate. 
	The script expects a link with text "Yes" in all pages; An "Add to cart" button on product pages, and a "Purchase" link in the checkout page
	The website used to develop this tool is available here: https://github.com/elenanesimm/demo_website

2) browser drivers installed on the machine.
	The location of the drivers is currently defined in the global vars of /elena_utils/utils.py:
	CHROME_DRIVER = '/usr/local/bin/chromedriver' 
	FIREFOX_DRIVER = '/usr/local/bin/geckodriver' 

3) install:
	python (eg: brew install python)
	open ssl (eg: brew install openssl)
	selenium (pip install selenium)


CONFIGURATION

1) use the demo_input.json file to customize the data playground. 
	IMPORTANT:
	- Change "BASE_URL" with the base URL you want to crawl (if you downloaded my demo_website, that might be under http://127.0.0.1/demo_project)
	- Change "GA_STREAM_ID" with the ID of the GA property you want to use (minus the "G-" prefix). This enables the creation of returning users

