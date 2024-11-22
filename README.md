# the_fairy_codemother (web data playground)
automation to create a realistic GA4 demo data set 

# INTRO

The script has 2 arguments: headless mode (0-1) and number of sessions (1+).

Eg: if the script is called as: 

	python app.py 0 4

it is going to simulate 4 sessions, without headless mode.

If arguments are missing, the script will run in headless mode, and choose the number of sessions (between 80 and 200) based on the day of the week.

Currently, this is (80, 100) for week days, and (150, 200) for week ends (fixed setup in app.py)

 # NOTE: It might take few scans for returning users to appear. 
 The first scans are needed to generate enough client_ids to simulate returning users. Currently the choice for new vs returning is set to 70-30 in Flask and 50-50 in MAMP:
 - at @app.before_request for the Flask website available here https://github.com/elenanesi/web_playground_flask
 - at line 28 of all pages for the localhost website https://github.com/elenanesi/demo_website

# INSTALLATION

To make this script work, you'll need to have 

1) A website to navigate.

2) Setup the config file "demo_input.json" adding the:
- URL of the website you want to visit
- URL to the sitemaps you want to use
- identifiers of the HTML elements you want to click
- identifiers of the cookie banner buttons
- desired distributions for dimensions (or leave as is)
- desired CVR for each acquisition source (or leave as is)
- campaign names (or leave as is)

3) install the following: (you can use pip install -r requirements.txt)
	- python (eg: brew install python)
	- playwright (pip install playwright)
 	- requests	


# CONFIGURATION

1) use the demo_input.json file to customize the data playground. 
	IMPORTANT:
	- Change "BASE_URL" with the base URL you want to crawl (if you downloaded my demo_website, that might be under http://127.0.0.1:8080).
	- use category and product sitemap to point to where the available pages are (leave as is if using the web_playground_flask in local)
	- use the selectors to specify how to identify the links to be clicked to add to cart and complete a purchase

2) Ensure your web server is on!

3) In order to have the tool visit the website every day, multiple times per day, you'll need to create a crontab. 
	You can create one by typing "crontab -e" in the terminal.
	Here's an example of mine:

	0 10 * * * /usr/bin/python3 /Users/elenanesi/Workspace/user-simulation/app.py > /dev/null 2>> Users/elenanesi/Workspace/user-simulation/logfile.log
