from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, JavascriptException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import csv
import re

def wait_for_clickable_element(driver, locator, timeout=100):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))

def login(driver):
    driver.get("https://token.unlocks.app/")
    sign_in_button = wait_for_clickable_element(driver, (By.XPATH, '/html/body/div[1]/div/div/div[2]/div/a/button/h5'))
    sign_in_button.click()
    next_page_button = wait_for_clickable_element(driver, (By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div/div/button[1]'))
    next_page_button.click()
    email_input = wait_for_clickable_element(driver, (By.TAG_NAME, 'input'))
    email_input.send_keys("roomtemp34@gmail.com")
    next_button_email = wait_for_clickable_element(driver, (By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button'))
    next_button_email.click()
    password_input = wait_for_clickable_element(driver, (By.CSS_SELECTOR, 'input[type="password"]'))
    password_input.send_keys("YtBpFmx$4aB")
    next_button_password = wait_for_clickable_element(driver, (By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button'))
    next_button_password.click()
    after_2fa_button = wait_for_clickable_element(driver, (By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div/div[2]/div/div/button'))
    after_2fa_button.click()

def navigate_and_click(driver):
    home_button = wait_for_clickable_element(driver, (By.XPATH, '/html/body/div[3]/div[2]/div[2]/div[1]/div[1]/button[1]/p'))
    home_button.click()
    sort_button = wait_for_clickable_element(driver, (By.XPATH, '/html/body/div[3]/div[2]/div[5]/table[2]/thead/tr/th[2]/div/div[1]'))
    sort_button.click()
    sort_button.click()  # Click again to ensure sorting order

def unwatch_token(driver):
    unwatch_button = wait_for_clickable_element(driver, (By.XPATH, '/html/body/div[3]/div[2]/div[5]/table[2]/tbody/tr[1]/td[1]/div'))
    unwatch_button.click()

def access_token_page(driver):
    token_button = wait_for_clickable_element(driver, (By.XPATH, '/html/body/div[3]/div[2]/div[5]/table[2]/tbody/tr[1]/td[2]/a'))
    token_button.click()

def scrape_data(driver):
    # Implementation remains the same, ensure to use wait_for_clickable_element for any new interactions
    # Note: The scraping logic and interactions within this function would need to be adjusted based on the page's structure and the data being scraped

if __name__ == '__main__':
    options = uc.ChromeOptions()
    options.add_argument("--disable-background-timer-throttling")
    driver = uc.Chrome(options=options)
    login(driver)
    driver.get('https://token.unlocks.app/')
    navigate_and_click(driver)
    access_token_page(driver)
    while True:
        scrape_data(driver)
        driver.get('https://token.unlocks.app/')
        navigate_and_click(driver)
        unwatch_token(driver)
        access_token_page(driver)
    driver.quit()