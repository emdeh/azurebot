from selenium import webdriver
from selenium.webdriver.edge.service import Service
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
    # Set up the Edge WebDriver Service
    service = Service(executable_path='C:\\Users\\mdehe\\Repos\\azurebot\\msedgedriver.exe')
    
    # Instantiate the Edge WebDriver
    driver = webdriver.Edge(service=service)
    attempt = 0
    
    while attempt < max_retries:
        try:
            # Navigate to the website
            driver.get("https://www.example.com")

            # Wait for the search box to be available
            wait = WebDriverWait(driver, 10)
            search_box = wait.until(EC.presence_of_element_located((By.NAME, "searchBoxName")))
            
            # Enter the search query and submit
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            
            # Wait for the results to load
            wait.until(EC.presence_of_element_located((By.ID, "resultsContainer")))
            results = driver.find_element(By.ID, "resultsContainer").text
            
            return results
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