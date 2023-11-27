from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO)

# Asynchronously execute calls to a pool of threads.
executor = ThreadPoolExecutor(max_workers=5)

async def async_search_website(query):
    loop = asyncio.get_event_loop()
    charity_info = await loop.run_in_executor(executor, search_website, query)
    return charity_info

def wait_for_element(driver, locator, timeout=10):
    """Wait for an element to be present and visible."""
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(locator),
            f"Element with locator {locator} not found in {timeout} seconds."
        )
    except TimeoutException as e:
        logging.exception("Timed out waiting for element: {0}".format(locator))
        raise e  # Re-raise exception to handle it in the calling function

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
            driver.get("https://www.acnc.gov.au/charity/charities")

            # Use efficient waits for elements
            search_box_locator = (By.CSS_SELECTOR, "input[placeholder='Search charity name or ABN']")
            wait_for_element(driver, search_box_locator)
            search_box = driver.find_element(*search_box_locator)
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)

            # Check if 'No charities found' message is displayed
            no_results_locator = (By.CSS_SELECTOR, ".alert-warning")
            if driver.find_elements(*no_results_locator):
                logging.info("No charities found matching the criteria.")
                return "No charities found matching your criteria."

            # Proceed with finding the table and charity link
            table_locator = (By.CLASS_NAME, "charities-table")
            wait_for_element(driver, table_locator)

            first_charity_link_locator = (By.CSS_SELECTOR, ".charities-table tbody tr:first-child a.name")
            wait_for_element(driver, first_charity_link_locator)
            for _ in range(3):  # Retry up to 3 times in case of stale element
                try:
                    first_charity_link = driver.find_element(*first_charity_link_locator)
                    logging.info("Clicking on the first charity link.")
                    first_charity_link.click()
                    break
                except StaleElementReferenceException:
                    logging.warning("Encountered StaleElementReferenceException, retrying...")
                    continue

            print_button_locator = (By.CSS_SELECTOR, "aside.charity-print button.btn-outline-success")
            wait_for_element(driver, print_button_locator)

            charity_details_div_locator = (By.CLASS_NAME, "charity-profile")
            charity_details_div = driver.find_element(*charity_details_div_locator)
            charity_details_text = charity_details_div.text

            return charity_details_text

        except (NoSuchElementException, TimeoutException, StaleElementReferenceException) as e:
            logging.exception("Error encountered during scraping: {0}".format(e))
            attempt += 1
        except Exception as e:
            logging.exception("Unexpected error occurred: {0}".format(e))
            break
        finally:
            driver.quit()
    
    return None  # Return None or appropriate fallback/error message if retries are exhausted
