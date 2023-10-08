# Scraping Comments from a DMP Online DMP

A Python script to scrape comments from DMP Online

## Getting started

### Setting up the login

To log in to DMP Online, we need cookies and headers. The easiest way for me was to use [curlconverter](https://curlconverter.com/)

1. Create the `config.py` file with cookies and headers (see `config.example.py`)
   1. Log in to DMP Online
   2. Go to https://dmponline.eur.nl/plans
   3. Open the DevTools. Go to the "Network" tab.
   4. Reload the page
   5. In the "Name" pane, look for the first request ("plans"). Right click the plan -> Copy -> Copy as cURL
2. Convert the cURL to a Python script, for `requests` using [curlconverter](https://curlconverter.com/)
3. Copy and paste the Python script to the `config.py` file. Make sure you have cookies and headers objects defined there.

⚠️ The cURL command contains credentials to login to DMP Online, and thus it's being ignored in git

### Scraping

Run the `scrape_comments.py`. It will create a pickle and JSON files that contains the results. Scraping may take around 5 minutes.
