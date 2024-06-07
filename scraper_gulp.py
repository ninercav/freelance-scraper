from selenium import webdriver
import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

        print("Number of projects:", len(paginated_list.find_elements(By.CLASS_NAME, 'project-item')))
        for job in driver.find_elements(By.CLASS_NAME, 'project-item'):
            title = job.find_element(By.TAG_NAME, 'app-heading-tag').text
            print("Title: ", title)

        

    except TimeoutException:
        print("Element not found within the given time.")

        time.sleep(100)
        # return relevant_projects

    finally:
        driver.quit()


if __name__ == '__main__':
    start_scraper('https://www.gulp.de/gulp2/g/projekte')
