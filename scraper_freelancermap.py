from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options

# each scraper has its own set of keywords? relocate to separate file?
relevant_keywords = ['Full stack', 'Backend', 'Java']

# work_type = ['Remote', 'Hybrid']
work_type = []
# work_type_exclude = ['Vor Ort', 'Onsite', 'Festanstellung']
work_type_exclude = []
title_keywords = []

freelancermap_urls = [
    'https://www.freelancermap.de/projektboerse.html?projectContractTypes%5B0%5D=contracting&matchingSkills%5B0%5D=KS120076FGP5WGWYMP0F&matchingSkills%5B1%5D=KSFFZBDYXH5XA5QE4E7I&countries%5B%5D=1&sort=1&pagenr=1'
]


def start_scraper(url) -> dict:
    # Initialize the Firefox options and set headless mode
    options = Options()
    options.headless = True

    # Initialize the WebDriver for Firefox
    service = FirefoxService(executable_path='geckodriver.exe')
    driver = webdriver.Firefox(service=service, options=options)

    try:
        driver.get(url)  # Get the website and generate the relevant HTML

        relevant_projects = {}

        print("Number of freelancermap projects: ", len(driver.find_elements(By.CLASS_NAME, 'project-container')))

        for job in driver.find_elements(By.CLASS_NAME, 'project-container'):
            title = job.find_element(By.CLASS_NAME, 'project-title').text
            company = job.find_element(By.CLASS_NAME, 'company').text
            location = job.find_element(By.CLASS_NAME, 'project-location').text
            keywords = []
            for keyword in job.find_elements(By.CLASS_NAME, 'keyword'):
                if keyword.get_attribute('data-tooltip-title'):
                    keywords.extend(keyword.get_attribute('data-tooltip-title').split('\n'))
                else:
                    keywords.append(keyword.text)

            # Check if the relevant keywords are in the project
            if work_type and not any(work in location for work in work_type):
                continue

            if work_type_exclude and any(work in location for work in work_type_exclude):
                continue

            if title_keywords and not any(title_keyword in title for title_keyword in title_keywords):
                continue

            if relevant_keywords and not any(keyword in keywords for keyword in relevant_keywords):
                continue

            relevant_projects[title] = {
                'company': company,
                'location': location,
                'keywords': keywords,
                'url': f'{job.find_element(By.CLASS_NAME, 'project-title').get_attribute("href")}'
            }

        return relevant_projects

    finally:
        # Ensure the driver is quit regardless of success or failure
        driver.quit()


def scrape_freelancermap() -> dict:
    relevant_projects = {}
    for url in freelancermap_urls:
        relevant_projects.update(start_scraper(url) or {})
    return relevant_projects
