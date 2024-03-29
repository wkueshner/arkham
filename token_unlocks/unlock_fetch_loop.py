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



def login(driver):
    # Navigate to the initial page
    driver.get("https://token.unlocks.app/")

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

    # Wait for 2FA to complete
    time.sleep(15) 

    # Click the Sign In button after 2FA verification
    after_2fa_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div/div[2]/div/div/button')
    after_2fa_button.click()

def navigate_and_click(driver):
    time.sleep(6) # wait until homepage is loaded
    # Clicks the button to navigate to the token list
    driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[2]/div[1]/div[1]/button[1]/p').click()
    time.sleep(4)  # Wait for the page to load
    # Clicks the button to sort the list
    sort_button = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[5]/table[2]/thead/tr/th[2]/div/div[1]')
    sort_button.click()
    time.sleep(4)  # Wait for sorting to take affect
    sort_button.click()  # Click again to set alphabetical-ascending sorting order

def unwatch_token(driver):
    # Unwatchlist the token
    time.sleep(3)  # Wait for the unwatch action to complete
    driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[5]/table[2]/tbody/tr[1]/td[1]/div').click()
    time.sleep(2)  # Wait for the unwatch action to complete

def access_token_page(driver):
    time.sleep(2)  # Wait for the token page to load
    # Accesses the token page
    token_button = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[5]/table[2]/tbody/tr[1]/td[2]/a')
    token_button.click()
    time.sleep(4)

def scrape_data(driver):
    # Scrape data from the graph and return to the main page
    # This function includes steps to locate the graph element, iterate across the chart, scrape data, and return to the main page
    # The implementation would be similar to the existing process in the script, adjusted for the new page structure if necessary

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

    # Open the CSV file for writing
    with open(csv_filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        print("CSV file opened for writing.")
        
        # Initialize a flag to track if the header has been written
        header_written = False

        # Now we iterate from the very right end of the graph to the very left end
        for x_offset in range(int(graph.size['width']) - 15, 62, -increment):
            print(f"Moving to x_offset: {x_offset}")
            # Move the mouse to the next position on the graph starting from the very right end
            actions.move_to_element_with_offset(graph, x_offset - (graph.size['width'] / 2), 10).perform()

            # Initialize variables for the loop to check for non-empty innerText
            max_wait_time = 5  # Maximum wait time in seconds
            check_interval = 0.1  # Time between checks in seconds
            elapsed_time = 0
            inner_text = ""

            try:
                tooltip = driver.find_element(By.CSS_SELECTOR, '#tp_chart_hover > div > div.\!p-0.\!bg-background.dark\:\!bg-background-dark.border-\[1px\].\!border-black-disabled.dark\:\!border-black-dark-disabled.\!rounded-\[8px\]')
                max_wait_time = 5  # Maximum wait time in seconds
                check_interval = 0.1  # Time between checks in seconds
                elapsed_time = 0
                inner_text = ""
                while elapsed_time < max_wait_time:
                    inner_text = driver.execute_script("return arguments[0].innerText", tooltip).strip()
                    if inner_text:  # Checks if innerText is not empty or undefined
                        break
                    time.sleep(check_interval)
                    elapsed_time += check_interval
                else:  # This block executes if the while loop completes without breaking
                    print("innerText was undefined")
                    continue
            except (JavascriptException, NoSuchElementException, StaleElementReferenceException, TimeoutException) as e:
                print(f"Exception encountered while waiting for non-empty tooltip text. Error details: {e}")
                continue  # Skip to the next iteration if an exception is encountered
                

            # Use the inner_text obtained from the loop
            tooltip_text = inner_text
            print(f"Tooltip text retrieved: {tooltip_text}")
            tooltip_text_modified = tooltip_text.replace("\nTBD", " (TBD)")
            lines = tooltip_text_modified.split('\n')

            # Write the header if it hasn't been written yet
            if not header_written:
                # Extract column names based on the specified line indices
                headers = ['Date', lines[2], lines[5]] # line 5/the third header may end up being "Allocations" if "Unlocked supply" does not exist
                additional_headers = [lines[i] for i in range(9, len(lines), 3)] # line 6/the fourth header may be a number if "Unlocked supply" does not exist, but this guarantees no important headers are missing
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
        
        # Clear the actions to avoid stacking commands
        actions = ActionChains(driver)

if __name__ == '__main__':
    options = uc.ChromeOptions()
    #options.add_argument("--headless")
    #options.add_argument("--window-size=1920,1080")  # Set your desired viewport size here
    options.add_argument("--disable-background-timer-throttling")  # Disable background throttling
    driver = uc.Chrome(options=options)

    size = driver.get_window_size()
    print("Window size:", size)  # Outputs: Window size: {'width': X, 'height': Y}
    width = driver.execute_script("return document.documentElement.clientWidth")
    height = driver.execute_script("return document.documentElement.clientHeight")
    print("Viewport size: {}x{}".format(width, height))

    #driver.set_window_size(1920, 1080)  # Set the desired viewport size here
    login(driver)
    driver.get('https://token.unlocks.app/')  # Navigate to the main page after login
    navigate_and_click(driver)
    access_token_page(driver)
    while True:
        scrape_data(driver)
        driver.get('https://token.unlocks.app/')  # Return to the main page to start the next iteration
        navigate_and_click(driver)
        unwatch_token(driver)
        access_token_page(driver)

    # Close the WebDriver
    driver.quit()

