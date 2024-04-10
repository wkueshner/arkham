#Note: before this script is run, all tokens on tokenunlocks must be watchlisted, as it works by unwatchlisting tokens when done

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, JavascriptException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
import csv
import re


js_function = """
function performDragActions(dragPoints) {
    console.log('performDragActions called with dragPoints:', dragPoints);
    dragPoints.forEach(([startX, startY, endX, endY], index) => {
        console.log('Starting drag action #' + (index + 1), 'from (' + startX + ', ' + startY + ') to (' + endX + ', ' + endY + ')');
        
        // Create the mousedown event
        const mouseDownEvent = new MouseEvent('mousedown', {
            bubbles: true,
            clientX: startX,
            clientY: startY,
        });
        console.log('mousedown event created');

        // Dispatch the mousedown event
        document.dispatchEvent(mouseDownEvent);
        console.log('mousedown event dispatched');

        // Create a series of mousemove events to simulate dragging
        const steps = 10; // Number of steps from start to end
        for (let i = 0; i <= steps; i++) {
            const moveX = startX + ((endX - startX) * i / steps);
            const moveY = startY + ((endY - startY) * i / steps);

            const mouseMoveEvent = new MouseEvent('mousemove', {
                bubbles: true,
                clientX: moveX,
                clientY: moveY,
            });
            console.log('mousemove event created for step', i);

            // Dispatch the mousemove event
            document.dispatchEvent(mouseMoveEvent);
            console.log('mousemove event dispatched for step', i);
        }

        // Create the mouseup event to release the drag
        const mouseUpEvent = new MouseEvent('mouseup', {
            bubbles: true,
            clientX: endX,
            clientY: endY,
        });
        console.log('mouseup event created');

        // Dispatch the mouseup event
        document.dispatchEvent(mouseUpEvent);
        console.log('mouseup event dispatched');
    });
    console.log('performDragActions completed');
}
"""

def login(driver):
    # Navigate to the initial page
    driver.get("https://token.unlocks.app/")

    time.sleep(4)
    '''
    viewport_width = driver.execute_script("return window.innerWidth")
    viewport_height = driver.execute_script("return window.innerHeight")
    print(f"Viewport size: {viewport_width}x{viewport_height}")
    '''
    # Wait for the sign in button to be clickable
    sign_in_button_xpath = '/html/body/div[2]/div/div/div[2]/div/a/button/h5' # Pre-banner:/html/body/div[1]/div/div/div[2]/div/a/button/h5' #'''
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, sign_in_button_xpath))).click()

    time.sleep(1)  # Added sleep

    # Wait for the next page button to be clickable and click it
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div/div/button[1]'))).click()

    time.sleep(1)  # Added sleep

    # Input email
    email_input = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.TAG_NAME, 'input')))  # Assuming the email input is the active/first input field
    email_input.send_keys("roomtemp34@gmail.com")

    time.sleep(1)  # Added sleep

    # Click the "Next" button after entering the email
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button'))).click()

    time.sleep(1)  # Added sleep

    # Input password
    password_input = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="password"]')))  # Targeting the password input specifically
    password_input.send_keys("YtBpFmx$4aB")

    time.sleep(1)  # Added sleep

    # Click the "Next" button after entering the password
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button'))).click()

    time.sleep(1)  # Added sleep

    # Wait for 2FA to complete and click the Sign In button after 2FA verification
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div/div[2]/div/div/button'))).click()

def navigate_and_click(driver):
    time.sleep(6) # wait until homepage is loaded
    # Clicks the button to navigate to the watched tokens list
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[2]/div[2]/div[1]/div[1]/button[1]/p'))).click()

    time.sleep(1)  # Added sleep

    # Clicks the button to sort the list
    sort_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[2]/div[5]/table[2]/thead/tr/th[2]/div/div[1]')))
    sort_button.click()
    time.sleep(1)  # Wait for sorting to take affect
    sort_button.click()  # Click again to set alphabetical-ascending sorting order

def unwatch_token(driver):
    # Unwatchlist the token
    time.sleep(2)  # Wait for the unwatch action to complete
    driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[5]/table[2]/tbody/tr[1]/td[1]/div').click()
    time.sleep(2)  # Wait for the unwatch action to complete

def access_token_page(driver):
    time.sleep(2) 
    # Accesses the token page
    token_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div[5]/table[2]/tbody/tr[1]/td[2]/a')))
    token_button.click()

def scrape_data(driver, is_first_call=True):
    # Scrape data from the graph and return to the main page
    # This function includes steps to locate the graph element, iterate across the chart, scrape data, and return to the main page
    # The implementation would be similar to the existing process in the script, adjusted for the new page structure if necessary
    # Fetch the initial innerText for the "Symbol"

    time.sleep(4) # wait for token page to load

    try:
        symbol_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[1]/div[1]/div/div[1]/div/span')))
        symbol_text = symbol_element.text
    except NoSuchElementException:
        print("Symbol element not found.")
        symbol_text = "N/A"  # Use "N/A" if the symbol element is not found

    # Attempt to click the standard allocations button, proceed accordingly based on outcome
    try:
        standard_allocations_button = WebDriverWait(driver, 12).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#tp_vestingallocation_toggle_basicallo > div > button')))
        allocations_button_clickable = True
    except TimeoutException:
        allocations_button_clickable = False
        print("Standard allocations button not clickable within 12 seconds.")

    url_slug = driver.current_url.split('/')[-1]

    if allocations_button_clickable:
        # If the button is clickable, proceed with the script and click the button
        driver.execute_script("arguments[0].click();", standard_allocations_button)
        time.sleep(2)
        if is_first_call:
            csv_filename = f"unlocks_standardized1/{url_slug}_standardized_unlock_schedule.csv" 
        else:
            csv_filename = f"unlocks1/{url_slug}_unlock_schedule.csv" 
    else:
        # If the button is not clickable within 20 seconds, proceed with the script without clicking the button
        # This part of the script will iterate just once in this case
        print("Proceeding without clicking the standard allocations button.")
        csv_filename = f"unlocks1/{url_slug}_unlock_schedule.csv" 

    # Locate the graph element where the tooltip appears
    try:
        graph = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tp_chart_hover')))
    except NoSuchElementException:
        print("Graph element not found.")
        driver.quit()
        raise

    # Scroll the graph element into view
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", graph)
    time.sleep(3)  # Wait a bit for the scroll action to complete

    # Initialize ActionChains for mouse movement
    actions = ActionChains(driver)

    # Choose the amount to move the cursor each time
    increment = 1

    # Open the CSV file for writing
    with open(csv_filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        print("CSV file opened for writing.")
        
        # Initialize a flag to track if the header has been written
        header_written = False
        
        for i in range(9):  # Loop for the initial and subsequent three iterations. Original: 7
            if i == 0:
                # Wait for the specific element on the first iteration
                target_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@id="tp_chart_hover"]//*[@width="2"][1]')))
                # Perform click_and_hold, drag 620 pixels to the right, and release
                ActionChains(driver).click_and_hold(target_element).move_by_offset(741, 0).release().perform() #Original: 715 (giving navbar a width of 128px)
            else:
                # Wait for the specific element on subsequent iterations
                target_element = WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.XPATH, '//div[@id="tp_chart_hover"]//*[@fill="#fff"]')))
                # Perform click_and_hold, drag 200 pixels to the left, and release
                ActionChains(driver).click_and_hold(target_element).move_by_offset(-100, 0).release().perform() #Original: -123. 710-(123*6)= -28 : full coverage
            
            # Add a delay to ensure the drag action has completed
            time.sleep(4)  # Adjust timing as necessary
            # Now we iterate from the very right end of the graph to the very left end
            for x_offset in range(int(graph.size['width']) - 63, 62, -increment):
                print(f"Moving to x_offset: {x_offset}")
                # Move the mouse to the next position on the graph starting from the very right end
                actions.move_to_element_with_offset(graph, x_offset - (graph.size['width'] / 2), 10).perform()

                try:
                    tooltip = driver.find_element(By.CSS_SELECTOR, '#tp_chart_hover > div > div.\!p-0.\!bg-background.dark\:\!bg-background-dark.border-\[1px\].\!border-black-disabled.dark\:\!border-black-dark-disabled.\!rounded-\[8px\]')
                    max_wait_time = 4  # Maximum wait time in seconds
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
                #print(f"Tooltip text retrieved: {tooltip_text}")
                tooltip_text_no_commas = tooltip_text.replace(",", "")
                tooltip_text_tbd_fix = tooltip_text_no_commas.replace("\nTBD", " (TBD)")
                #print(f"Tooltip text modified: {tooltip_text_tbd_fix}")
                tooltip_text_no_symbols = re.sub(r'(\.\d{2}).*?(?=\n|$)', r'\1', tooltip_text_tbd_fix)
                print(f"Tooltip text without symbols: {tooltip_text_no_symbols}")
                lines = tooltip_text_no_symbols.split('\n')

                # Write the header if it hasn't been written yet
                if not header_written:
                    # Extract column names based on the specified line indices
                    headers = ['Date', 'Symbol', 'Price', lines[2], lines[5]] # line 5/the third header may end up being "Allocations" if "Unlocked supply" does not exist
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
                    data_for_headers["Symbol"] = symbol_text  # Assign the fetched symbol text to the "Symbol" header

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
        
        if allocations_button_clickable and is_first_call:
            # Call the scrape_data function again to repeat the process, but only if it's the first call
            scrape_data(driver, is_first_call=False)

if __name__ == '__main__':
    options = uc.ChromeOptions()
    #options.add_argument("--headless")
    #options.add_argument("--window-size=1920,1080")  # Set your desired viewport size here
    options.add_argument("--disable-background-timer-throttling")  # Disable background throttling
    driver = uc.Chrome(options=options)
    driver.set_window_position(-10000, 10000)

    """size = driver.get_window_size()
    print("Window size:", size)  # Outputs: Window size: {'width': X, 'height': Y}
    width = driver.execute_script("return document.documentElement.clientWidth")
    height = driver.execute_script("return document.documentElement.clientHeight")
    print("Viewport size: {}x{}".format(width, height))
    """

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
    driver.quit



