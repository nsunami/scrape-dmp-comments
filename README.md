# Scraping Comments from DMP Online

A Python script to scrape comments from DMP Online (at Erasmus University Rotterdam)

## Getting started

### Setting up the login

To log in to DMP Online, we need cookies and headers.

1. Create the `config.py` file.
2. You need to save cookies and headers to this file (see `config.example.py`). You can get the cURL, and convert it via [curlconverter](https://curlconverter.com/). To get the cURL, do the following:
   1. Log in to DMP Online
   2. Go to https://dmponline.eur.nl/plans
   3. Open the DevTools. Go to the "Network" tab.
   4. Reload the page
   5. In the "Name" pane, look for the first request ("plans"). Right click the plan -> Copy -> Copy as cURL
3. Copy and paste the Python script to the `config.py` file. You only need `cookies` and `headers` dictionaries.

⚠️ The cURL command contains credentials to login to DMP Online, and thus it's being ignored in git

### Scraping

Run the `scrape_comments.py`. It will create a pickle and JSON files that contains the results. Scraping may take around 5 minutes. Note that the script only gets comments from DMPs using EUR's v4.5 DMP Template only.
