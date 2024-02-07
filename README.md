# demo_dataset (web data playground)
automation to create a realistic GA4 demo data set 

# INTRO

The script has 2 arguments: headless mode (0-1) and number of sessions (1+).

Eg: if the script is called as: 

	python simulate_users.py 0 4

it is going to simulate 4 sessions, without headless mode.

If arguments are missing, the script will run in headless mode, and choose the number of sessions (between 80 and 200) based on the day of the week.

Currently, this is (80, 100) for week days, and (150, 200) for week ends (fixed setup in simulate_users.py)

# INSTALLATION

To make this script work, you'll need to have 

1) A localhost website to navigate. 
	The script expects a link with text "Yes" in all pages; An "Add to cart" button on product pages, and a "Purchase" link in the checkout page
	The website used to develop this tool is available here: https://github.com/elenanesimm/demo_website

2) browser drivers installed on the machine.
	you can get them here: 
	- https://googlechromelabs.github.io/chrome-for-testing/
	- https://github.com/mozilla/geckodriver/releases
	
	The location of the drivers is currently defined in the global vars of /elena_utils/utils.py:
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
	- Change "GA_STREAM_ID" with the ID of the GA stream ID you want to use (minus the "G-" prefix). This enables the creation of returning users

2) Ensure your web server is on!

3) In order to have the tool visit the website every day, multiple times per day, you'll need to create a crontab. 
	You can create one by typing "crontab -e" in the terminal.
	Here's an example of mine:

	0 10 * * * /usr/bin/python3 /Users/elenanesi/Workspace/user-simulation/simulate_users.py > /dev/null 2>> Users/elenanesi/Workspace/user-simulation/logfile.log
	30 10 * * * /usr/bin/python3 /Users/elenanesi/Workspace/user-simulation/simulate_users.py > /dev/null 2>> Users/elenanesi/Workspace/user-simulation/logfile.log
	0 11 * * * /usr/bin/python3 /Users/elenanesi/Workspace/user-simulation/simulate_users.py > /dev/null 2>> Users/elenanesi/Workspace/user-simulation/logfile.log
	30 11 * * * /usr/bin/python3 /Users/elenanesi/Workspace/user-simulation/simulate_users.py > /dev/null 2>> Users/elenanesi/Workspace/user-simulation/logfile.log
	0 12 * * * /usr/bin/python3 /Users/elenanesi/Workspace/user-simulation/simulate_users.py > /dev/null 2>> Users/elenanesi/Workspace/user-simulation/logfile.log
	30 12 * * * /usr/bin/python3 /Users/elenanesi/Workspace/user-simulation/simulate_users.py > /dev/null 2>> Users/elenanesi/Workspace/user-simulation/logfile.log
	0 13 * * * /usr/bin/python3 /Users/elenanesi/Workspace/user-simulation/simulate_users.py > /dev/null 2>> Users/elenanesi/Workspace/user-simulation/logfile.log
	30 13 * * * /usr/bin/python3 /Users/elenanesi/Workspace/user-simulation/simulate_users.py > /dev/null 2>> Users/elenanesi/Workspace/user-simulation/logfile.log
	0 14 * * * /usr/bin/python3 /Users/elenanesi/Workspace/user-simulation/simulate_users.py > /dev/null 2>> Users/elenanesi/Workspace/user-simulation/logfile.log
	30 14 * * * /usr/bin/python3 /Users/elenanesi/Workspace/user-simulation/simulate_users.py > /dev/null 2>> Users/elenanesi/Workspace/user-simulation/logfile.log
	0 15 * * * /usr/bin/python3 /Users/elenanesi/Workspace/user-simulation/simulate_users.py > /dev/null 2>> Users/elenanesi/Workspace/user-simulation/logfile.log
	30 15 * * * /usr/bin/python3 /Users/elenanesi/Workspace/user-simulation/simulate_users.py > /dev/null 2>> Users/elenanesi/Workspace/user-simulation/logfile.log
	0 16 * * * /usr/bin/python3 /Users/elenanesi/Workspace/user-simulation/simulate_users.py > /dev/null 2>> Users/elenanesi/Workspace/user-simulation/logfile.log
	30 16 * * * /usr/bin/python3 /Users/elenanesi/Workspace/user-simulation/simulate_users.py > /dev/null 2>> Users/elenanesi/Workspace/user-simulation/logfile.log
	0 17 * * * /usr/bin/python3 /Users/elenanesi/Workspace/user-simulation/simulate_users.py > /dev/null 2>> Users/elenanesi/Workspace/user-simulation/logfile.log
	30 17 * * * /usr/bin/python3 /Users/elenanesi/Workspace/user-simulation/simulate_users.py > /dev/null 2>> Users/elenanesi/Workspace/user-simulation/logfile.log
	0 18 * * * /usr/bin/python3 /Users/elenanesi/Workspace/user-simulation/simulate_users.py > /dev/null 2>> Users/elenanesi/Workspace/user-simulation/logfile.log
	30 18 * * * /usr/bin/python3 /Users/elenanesi/Workspace/user-simulation/simulate_users.py > /dev/null 2>> Users/elenanesi/Workspace/user-simulation/logfile.log
	0 19 * * * /usr/bin/python3 /Users/elenanesi/Workspace/user-simulation/simulate_users.py > /dev/null 2>> Users/elenanesi/Workspace/user-simulation/logfile.log
	30 19 * * * /usr/bin/python3 /Users/elenanesi/Workspace/user-simulation/simulate_users.py > /dev/null 2>> Users/elenanesi/Workspace/user-simulation/logfile.log
	0 20 * * * /usr/bin/python3 /Users/elenanesi/Workspace/user-simulation/simulate_users.py > /dev/null 2>> Users/elenanesi/Workspace/user-simulation/logfile.log
	30 20 * * * /usr/bin/python3 /Users/elenanesi/Workspace/user-simulation/simulate_users.py > /dev/null 2>> Users/elenanesi/Workspace/user-simulation/logfile.log
	0 21 * * * /usr/bin/python3 /Users/elenanesi/Workspace/user-simulation/simulate_users.py > /dev/null 2>> Users/elenanesi/Workspace/user-simulation/logfile.log
	30 21 * * * /usr/bin/python3 /Users/elenanesi/Workspace/user-simulation/simulate_users.py > /dev/null 2>> Users/elenanesi/Workspace/user-simulation/logfile.log 

