# Freelance Scraper
The freelance scraper is a python script that scrapes the freelance website [freelancer.com](https://www.freelancer.com/) for projects that match a given search query. The script uses the selenium package to scrape the website at regular intervals and the smtplib package to send an email with the results.

## Setup
To run the python script, Python3 has to be installed. The required packages are located in [requirements.txt](requirements.txt).
For selenium to work, a driver has to be installed (e.g. [geckodriver](https://github.com/mozilla/geckodriver/releases) for Firefox or [chromedriver](https://developer.chrome.com/docs/chromedriver/downloads) for Chrome).
The driver should be installed in the root directory of the project.

### Email service password
The password for the email account isn't stored in the repository for security reasons. It should be added as an environment variable before running the script.

## Usage
The script can be run with the following command:
```bash
python scraper.py
```