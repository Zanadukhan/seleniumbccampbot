import time
import string
import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



PARK = string.capwords('E.C. Manning')
MONTH = 'jun'.capitalize()
START_DATE = '15'
END_DATE = '17'
CAMPSITE_NAME = 'Coldspring'
# limitation: requires full name if the campsite name isn't descriptive enough
# ie instead of 'B', needs to be 'B (Sites 56-96)'
# leave CAMPSITE_NAME empty if there is no multiple campsites to choose from


driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

driver.get('https://camping.bcparks.ca/')

email = os.environ.get('BC_EMAIL')
password = os.environ.get('BC_PASSWORD')

# removes the cookie notification
driver.find_element(By.CSS_SELECTOR, '#consentButton').click()




#login function commented out for testing purposes
# WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#login"))).click()

# waits until the screen transitions to the login screen and logs in user
# WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#email"))).send_keys(f'{email}')
# password_entry = driver.find_element(By.CSS_SELECTOR, '#password')
# password_entry.send_keys(f'{password}')
# driver.find_element(By.CSS_SELECTOR, '#loginButton').click()

# takes you back to reservation screen
# WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#newReservation"))).click()
# uncomment everything above here for login functionality

# entering reservation information
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#park-autocomplete")))\
    .clear()

# for some reason, I have to separate these two or clear() prevents send_keys from functioning
# Inputs park name
driver.find_element(By.CSS_SELECTOR, "#park-autocomplete").send_keys(f'{PARK}')


# enters desired date
driver.find_element(By.CSS_SELECTOR, '#mat-date-range-input-0').click()
driver.find_element(By.CSS_SELECTOR, '#monthDropdownPicker').click()
driver.find_element(By.XPATH,f".//button[contains(@aria-label,'{MONTH}')]").click()
driver.find_element(By.XPATH, f"//button[normalize-space()='{START_DATE}']").click()
driver.find_element(By.XPATH, f'//button[normalize-space()="{END_DATE}"]').click()


#equipment entry
driver.find_element(By.CSS_SELECTOR, '#equipment-field').click()
driver.find_element(By.XPATH, "//span[contains(text(), '2 Tents')]").click()

#search
driver.find_element(By.CSS_SELECTOR, '#actionSearch').click()
# give the site time to refresh
time.sleep(2)
# displays list of campsites
driver.find_element(By.CSS_SELECTOR, '#list-view-button').click()
time.sleep(2)
driver.find_element(By.XPATH, f"//*[contains(text(), '{CAMPSITE_NAME}')]").click()

# filter out double booking sites
driver.find_element(By.CSS_SELECTOR, '#filtersButton').click()
driver.find_element(By.CSS_SELECTOR, '#mat-radio-8').click()
driver.find_element(By.CSS_SELECTOR, '#confirmButton').click()

# opens up first entry on the list and takes you to reservation screen
WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CLASS_NAME, "list-entry"))).click()
driver.find_element(By.CSS_SELECTOR, '#reserveButton-0').click()

# checks both checkboxes and takes you to shopping cart
time.sleep(1.5)
checkboxes = driver.find_elements(By.CLASS_NAME, 'mat-checkbox-inner-container')
for checkbox in checkboxes:
    checkbox.click()
driver.find_element(By.CSS_SELECTOR, '#confirmReservationDetails').click()