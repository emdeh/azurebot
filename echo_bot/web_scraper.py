from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import logging
import time


# Configure logging
logging.basicConfig(level=logging.INFO)

def search_website(query, max_retries=3):
    # Configure Edge in headless mode
    options = EdgeOptions()
    options.use_chromium = True  # If you're using Chromium-based Edge
    options.add_argument("headless")
    options.add_argument("disable-gpu")  # Optional, needed on some systems

    # Set up the Edge WebDriver Service with headless options
    service = Service(executable_path='C:\\Users\\mdehe\\Repos\\azurebot\\msedgedriver.exe')
    driver = webdriver.Edge(service=service, options=options)

    attempt = 0
    
    while attempt < max_retries:
        try:
            # Navigate to the website
            driver.get("https://www.acnc.gov.au/charity/charities")

            # Wait for the search box to be available
            wait = WebDriverWait(driver, 10)
            search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Search charity name or ABN']")))
            
            # Enter the search query and submit
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            
            # Wait for the charities table to load
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "charities-table")))

            # Find the first charity name link in the table and click it
            first_charity_link = driver.find_element(By.CSS_SELECTOR, ".charities-table tbody tr:first-child .name")
            first_charity_link.click()

            # Wait for the 'Print Charity Details' button within the 'charity-print' aside to be visible
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "aside.charity-print button.btn-outline-success")))

            # Locate the div containing the charity information and extract its text
            charity_details_div = driver.find_element(By.CLASS_NAME, "charity-profile")
            charity_details_text = charity_details_div.text
            
            # Print or return the extracted text
            return charity_details_text

        except (NoSuchElementException, TimeoutException) as e:
            logging.exception(f"Error encountered while trying to scrape the website: {e}")
            attempt += 1
            time.sleep(5)  # Wait a bit before retrying
        except Exception as e:
            logging.exception(f"An unexpected error occurred: {e}")
            break
        finally:
            # Close the WebDriver
            driver.quit()
    
    return None  # or an appropriate fallback/error message