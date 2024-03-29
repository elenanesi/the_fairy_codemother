# the_fairy_codemother (web data playground)
automation to create a realistic GA4 demo data set 

# INTRO

The script has 2 arguments: headless mode (0-1) and number of sessions (1+).

Eg: if the script is called as: 

	python simulate_users.py 0 4

it is going to simulate 4 sessions, without headless mode.

If arguments are missing, the script will run in headless mode, and choose the number of sessions (between 80 and 200) based on the day of the week.

Currently, this is (80, 100) for week days, and (150, 200) for week ends (fixed setup in simulate_users.py)

 # NOTE: It might take few scans for returning users to appear. 
 The first scans are needed to generate enough client_ids to simulate returning users. Currently the choice for new vs returning is set to 50-50, within the demo website at line 28 of all pages of https://github.com/elenanesi/web_playground

# INSTALLATION

To make this script work, you'll need to have 

1) A localhost website to navigate. 
	The script expects a link with text "Yes" in all pages; An "Add to cart" button on product pages, and a "Purchase" link in the checkout page
	The website used to develop this tool is available here: https://github.com/elenanesimm/web_playground

2) install the browser drivers on your machine; move them in /usr/local/bin/ (or wherever your terminal has access to, but then remember to update demo_input.json)
	NOTE: 
	- the version of the driver should match the version on the browser you have installed.
	- ensure they can be opened (might need explicit admin access)
	- might need to quarantine drivers on MAC: xattr -d com.apple.quarantine chromedrive
	
	you can get the drivers here: 
	- https://googlechromelabs.github.io/chrome-for-testing/
	- https://github.com/mozilla/geckodriver/releases

	The location of the drivers can be changed from the demo_input.json file.
	The default value is currently defined in the global vars of /elena_utils/utils.py:
	- CHROME_DRIVER = '/usr/local/bin/chromedriver' 
	- FIREFOX_DRIVER = '/usr/local/bin/geckodriver' 

3) install:
	- python (eg: brew install python)
	- open ssl (eg: brew install openssl)
	- selenium (pip install selenium)


# CONFIGURATION

1) use the demo_input.json file to customize the data playground. 
	IMPORTANT:
	- Change "BASE_URL" with the base URL you want to crawl (if you downloaded my demo_website, that might be under http://127.0.0.1/demo_project)
	- Change "GA_MEASUREMENT_ID" with the ID of the GA MEASUREMENT ID you want to use (minus the "G-" prefix). This enables the creation of returning users

2) Ensure your web server is on!

3) In order to have the tool visit the website every day, multiple times per day, you'll need to create a crontab. 
	You can create one by typing "crontab -e" in the terminal.
	Here's an example of mine:

	0 19 * * * cd /Users/elenanesi/Workspace/user-simulation && /Users/elenanesi/.pyenv/shims/python3 simulate_users.py > output.log 2>> logfile.log



