# Freelance Scraper
The freelance scraper is a python script that scrapes the freelance websites [freelancermap](https://www.freelancermap.de) and [gulp](https://www.gulp.de/) for projects that match a given search query. The script uses the selenium package to scrape the website at regular intervals and the smtplib package to send an email with the results.

Due to registration limitations, only the first page of projects can be loaded.

## Setup
To run the python script, Python3 has to be installed. The required packages are located in [requirements.txt](requirements.txt).
For selenium to work, the [geckodriver](https://github.com/mozilla/geckodriver/releases) has to be downloaded for Firefox.
The driver should be downloaded in the root directory of the project.

### Email service password
The credentials for the email account aren't stored in the repository for security reasons. They should be added as an environment variable before running the script (the scraper uses a gmail account to send the email). The following environment variables should be set:

    GMAIL_ADDRESS=example_addr@gmail.com
    GMAIL_PASSWORD=password
    POLL_INTERVAL=30 # in seconds, default if not provided is 30 seconds

The gmail password should be an app password, as the script uses the smtplib package to send the email (see [further info](https://support.google.com/mail/answer/185833?hl=en)).

## Usage
The script can be run with the following command:
```bash
python scraper.py
```