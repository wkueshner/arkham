from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, JavascriptException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
import csv
import re
import os

driver = uc.Chrome()
driver.set_window_size(1920, 1080)  # Set the desired viewport size here

# Navigate to the initial page
driver.get("https://token.unlocks.app/arbitrum")

time.sleep(3)  # Adjust based on page load times

# Wait for the sign in button to be clickable
sign_in_button_xpath = '/html/body/div[1]/div/div/div[2]/div/a/button/h5'
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, sign_in_button_xpath)))

# Refetch the sign in button to get a fresh reference and then click it
sign_in_button = driver.find_element(By.XPATH, sign_in_button_xpath)
sign_in_button.click()

# Wait for the next page to load and click the button
time.sleep(6)  # Adjust based on your internet speed
next_page_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div/div/button[1]')
next_page_button.click()

# Input email
time.sleep(3)  # Adjust based on page load times
email_input = driver.find_element(By.TAG_NAME, 'input')  # Assuming the email input is the active/first input field
email_input.send_keys("wkueshner@gmail.com")


time.sleep(6)  # Adjust based on page load times

# Click the "Next" button after entering the email
next_button_email = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button')
next_button_email.click()

# Input password
time.sleep(6)  # Adjust based on page load times
password_input = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')  # Targeting the password input specifically
password_input.send_keys("u3DeqMrHNqcG")


time.sleep(4)  # Adjust based on page load times
# Click the "Next" button after entering the password
next_button_password = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button')
next_button_password.click()

# Wait for 2FA verification
time.sleep(20)  # Adjust this sleep time as needed for 2FA

# Click the button after 2FA verification
after_2fa_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div/div[2]/div/div/button')
after_2fa_button.click()

# Navigate to the page again now that cookies are loaded
driver.get('https://token.unlocks.app/arbitrum')
time.sleep(2)  # Wait for any post-login redirects

# Locate the graph element where the tooltip appears
try:
    graph = driver.find_element(By.CSS_SELECTOR, '#tp_chart_hover')
except NoSuchElementException:
    print("Graph element not found.")
    driver.quit()
    raise
# Determine the range of movement over the graph
start_x = graph.location['x']
end_x = start_x + graph.size['width']

# Choose the amount to move the cursor each time
increment = 1

# Initialize ActionChains for mouse movement
actions = ActionChains(driver)

# Get the URL slug for the CSV filename
url_slug = driver.current_url.split('/')[-1]
csv_filename = f"unlocks/{url_slug}_unlock_schedule.csv"

# Ensure the directory exists
os.makedirs(os.path.dirname(csv_filename), exist_ok=True)

# Open the CSV file for writing
with open(csv_filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    print("CSV file opened for writing.")
    
    # Initialize a flag to track if the header has been written
    header_written = False

    # Now we iterate from the very right end of the graph to the very left end
    for x_offset in range(int(graph.size['width']) - 17, 62, -increment):
        print(f"Moving to x_offset: {x_offset}")
        # Move the mouse to the next position on the graph starting from the very right end
        actions.move_to_element_with_offset(graph, x_offset - (graph.size['width'] / 2), 10).perform()  # Adjusting x_offset to start from the right end, Y-offset is an arbitrary small number inside the graph

        # Since the tooltip is hidden, we need to wait for it to become visible after moving the cursor
        try:
            tooltip = driver.find_element(By.CSS_SELECTOR, '#tp_chart_hover > div > div.\!p-0.\!bg-background.dark\:\!bg-background-dark.border-\[1px\].\!border-black-disabled.dark\:\!border-black-dark-disabled.\!rounded-\[8px\]')
            elapsed_time = 0
            sleep_time = 0.25 #previous start: 1 second
            max_wait_time = 6 #previous max: 10 seconds
            while elapsed_time < max_wait_time:
                inner_text = driver.execute_script("return arguments[0].innerText", tooltip).strip()
                if inner_text:  # Checks if innerText is not empty or undefined
                    break
                time.sleep(sleep_time)
                elapsed_time += sleep_time
                sleep_time = min(sleep_time * 2, max_wait_time - elapsed_time)  # Double the sleep time but do not exceed max_wait_time
            else:  # This block executes if the while loop completes without breaking
                print("innerText was undefined")
                continue
        except (JavascriptException, NoSuchElementException, StaleElementReferenceException) as e:
            print(f"Exception encountered while trying to find the tooltip. Error details: {e}")
            continue
        # Check if the tooltip is displayed before attempting to scrape content
        if driver.execute_script("return arguments[0].style.opacity", tooltip) != '0':
            tooltip_text = driver.execute_script("return arguments[0].innerText", tooltip)
            print(f"Tooltip text retrieved: {tooltip_text}")
            tooltip_text_modified = tooltip_text.replace("\nTBD", " (TBD)")
            lines = tooltip_text_modified.split('\n')
            # Write the header if it hasn't been written yet
            if not header_written:
                # Extract column names based on the specified line indices
                headers = ['Date', lines[2], lines[5], lines[6]]
                additional_headers = [lines[i] for i in range(9, len(lines), 3)]
                headers.extend(additional_headers)
                csvwriter.writerow(headers)
                print("Header written to CSV.")
                header_written = True
            
            # Initialize a dictionary to hold the data for each header
            data_for_headers = {header: 0 for header in headers}  # Start with 0 for all headers

            # Assign the first line to the "Date" header explicitly
            if lines:  # Ensure there is at least one line
                data_for_headers["Date"] = lines[0]

            # Iterate through lines to find matches and assign data
            for i in range(1, len(lines)):  # Start from 1 since we check the preceding line
                preceding_line = lines[i - 1]
                current_line = lines[i]
                if preceding_line in headers:
                    # If the preceding line is a header, assign the current line's data to it
                    data_for_headers[preceding_line] = current_line

            # Prepare the data row in the order of headers
            data_row = [data_for_headers[header] for header in headers]

            # Write the data row to the CSV
            csvwriter.writerow(data_row)
            print("Data row written to CSV.")
        else:
            # If the tooltip is not visible, write a row indicating this
            print("Tooltip not visible.")
            if not header_written:
                # Write a header with a single column
                csvwriter.writerow(['Info'])
                print("Single column header written to CSV.")
                header_written = True
            csvwriter.writerow(['Tooltip not visible'])

        # Clear the actions to avoid stacking commands
        actions = ActionChains(driver)


# Close the WebDriver
driver.quit()

if __name__ == '__main__':
    # Configure Selenium to use Chrome
    chrome_options = Options()
    #chrome_options.add_argument("--headless")  # Remove or comment out this line to run in headed mode

    # Initialize the Chrome WebDriver
    driver_path = '/Users/wku/crypto-intel/arkham/chromedriver/mac_arm-123.0.6312.58/chromedriver-mac-arm64/chromedriver'  # Update this path
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Your code to interact with the page goes here
        pass
    finally:
        driver.quit
