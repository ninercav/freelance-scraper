from selenium import webdriver
import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

gulp_urls = [
    'https://www.gulp.de/gulp2/g/projekte?query=Java,%20Backend,%20Full%20stack'
]

def start_scraper(url) -> dict:
    options = Options()
    options.headless = True

    service = FirefoxService(executable_path='geckodriver.exe')
    driver = webdriver.Firefox(service=service, options=options)

    try:
        driver.get(url)

        wait = WebDriverWait(driver, 10)  # wait for a maximum of 10 seconds
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'paginated-list-container')))

        paginated_list = driver.find_element(By.CLASS_NAME, 'paginated-list-container')

        print("Number of gulp projects:", len(paginated_list.find_elements(By.CLASS_NAME, 'project-item')))

        relevant_projects = {}

        for job in driver.find_elements(By.CLASS_NAME, 'project-item'):
            title = job.find_element(By.TAG_NAME, 'app-heading-tag').text

            project_info = {}

            # get all infoListItems (li elements) from app-icon-info-list card
            app_icon_info_list = job.find_element(By.TAG_NAME, 'app-icon-info-list')
            info_list_items = app_icon_info_list.find_elements(By.TAG_NAME, 'li')
            for item in info_list_items:
                if 'Project Provider' in item.text:
                    project_info['company'] = item.text.split(':')[1].strip()
                if 'Location' in item.text:
                    project_info['location'] = item.text.split(':')[1].strip()
                if 'Start Date' in item.text:
                    project_info['start_date'] = item.text.split(':')[1].strip()

            url = job.find_element(By.TAG_NAME, 'app-heading-tag').find_element(By.TAG_NAME, 'h1').find_element(By.TAG_NAME, 'a').get_attribute('href')
            project_info['url'] = f'{url}'

            relevant_projects.update({title: project_info})

        return relevant_projects
        

    except TimeoutException:
        print("Element not found within the given time.")

        time.sleep(100)

    finally:
        driver.quit()

def scrape_gulp() -> dict:
    relevant_projects = {}
    for url in gulp_urls:
        relevant_projects.update(start_scraper(url) or {})
    return relevant_projects
