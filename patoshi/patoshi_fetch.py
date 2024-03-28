from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import csv

from bs4 import BeautifulSoup
import time

def get_block_info(block_number, driver):
    url = f'http://satoshiblocks.info/?bn={block_number}'
    
    max_retries = 3  # Maximum number of retries
    retries = 0
    
    while retries < max_retries:
        driver.get(url)
        
        # Use BeautifulSoup to parse the page source HTML
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        try:
            div_content_html = soup.select_one('body > table > tbody > tr > td:nth-child(1) > div:nth-child(2) > div:nth-child(2)').decode_contents()
            
            # Splitting based on the appearance of </a>
            parts = div_content_html.split('</a>', 1)  # Split at the first occurrence of </a>
            if len(parts) > 1:
                entity_html = parts[0] + '</a>'  # Optionally add </a> back to entity part
                ExtraNonce_html = parts[1]
                
                entity = BeautifulSoup(entity_html, 'html.parser').get_text().strip()
                ExtraNonce = BeautifulSoup(ExtraNonce_html, 'html.parser').get_text().strip()
                
                if entity == "" or ExtraNonce == "":
                    entity, ExtraNonce = "Not found", "Not found"
                else:
                    return entity, ExtraNonce
            else:
                entity, ExtraNonce = "Not found", "Not found"
            
            if entity == "Not found" or ExtraNonce == "Not found":
                retries += 1
                time.sleep(0.5)  # Wait for half a second before retrying
                continue
            else:
                return entity, ExtraNonce
        except Exception as e:
            print(f"Error processing block number {block_number}: {str(e)}")
            return "Error", "Error"

    return entity, ExtraNonce  # Return the last attempt's result if all retries fail



def main():
    # Configure Selenium to use Chrome in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    
    # Initialize the Chrome WebDriver
    driver_path = '/Users/wku/crypto-intel/arkham/chromedriver/mac_arm-123.0.6312.58/chromedriver-mac-arm64/chromedriver'  # Adjust if your path is different
    s = Service(driver_path)
    driver = webdriver.Chrome(service=s, options=chrome_options)
    
    # Open a CSV file to save the results
    with open('block_info.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['block_height', 'entity', 'ExtraNonce'])
        
        # Iterate over block numbers from 0 to 49999
        for block_number in range(4667, 50000):
            entity, ExtraNonce = get_block_info(block_number, driver)
            # Write the block number and content to the CSV
            writer.writerow([block_number, entity, ExtraNonce])
            print(f"Processed block number {block_number}")

    # Close the browser window
    driver.quit()

if __name__ == '__main__':
    main()
