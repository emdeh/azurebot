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
    options.add_experimental_option("excludeSwitches", ["enable-logging"]) # This excludes the 'enable-logging' switch from the command line arguments passed to the WebDriver executable

    # Set up the Edge WebDriver Service with headless options
    service = Service(executable_path='C:\\Users\\mdehe\\Repos\\azurebot\\msedgedriver.exe')
    driver = webdriver.Edge(service=service, options=options)

    attempt = 0
    
    while attempt < max_retries:
        try:
            # Navigate to the website
            driver.get("https://www.gg.org.au/find-a-charity/advanced-search")

            # Wait for the search box to be available
            wait = WebDriverWait(driver, 10)
            search_box = wait.until(EC.presence_of_element_located((By.ID, "searchTerms")))
            
            # Enter the search query and submit
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            
            # Wait for the specific section containing the container to load
            section_xpath = "//section[.//div[@class='container']]"
            wait.until(EC.presence_of_element_located((By.XPATH, section_xpath)))

            # Find the first charity name link in the table and click it
            first_charity_link = driver.find_element(By.CSS_SELECTOR, "td.labes .labes_inner h5 a")
            first_charity_link.click()

            # Wait for the ACNC logo link to be visible
            acnc_logo_link_xpath = "//a[contains(@href, '/charity/charities') and @target='_blank']"
            wait.until(EC.presence_of_element_located((By.XPATH, acnc_logo_link_xpath)))

            # List of section class names to extract data from
            section_classes = ["key_info", "more_details mt-5", "expenses pt-5", "charity_programs_wrap", "key_people"]

            # Initialize an empty string to accumulate text from each section
            charity_details_text = ""

            # Find all section elements for each class and extract their text
            for section_class in section_classes:
                if ' ' in section_class:  # If the class name contains a space (multiple classes)
                    sections = driver.find_elements(By.CSS_SELECTOR, f".{section_class.replace(' ', '.')}")
                else:  # If it's a single class name
                    sections = driver.find_elements(By.CLASS_NAME, section_class)

                for section in sections:
                    charity_details_text += section.text + "\n\n"

            # Remove trailing newlines if necessary
            charity_details_text = charity_details_text.strip()
            
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