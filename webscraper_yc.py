from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import csv

driver = webdriver.Chrome()

#ask for YC batch number
batch = input("Enter YC batch number(eg. S23/W21): ")
base_url = "https://www.ycombinator.com/companies?batch="
url = base_url + batch
driver.get(url)
# to allow loading of content
scroll_pause_time = 1
elements = driver.find_element(By.CLASS_NAME, 'q1vdpoLtJkwUT8jN22K2.dsStC1AzZueqISZqfHLZ')

def format_hyperlink(url):
    # Format the URL as a hyperlink in Excel
    return f'=HYPERLINK("{url}","YC Profile")'

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "WxyYeI15LZ5U_DOM0z8F"))
    )
finally:
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(scroll_pause_time)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    # get all the companies
    companies = elements.find_elements(By.CLASS_NAME,"WxyYeI15LZ5U_DOM0z8F")
    # get text from each company
    names = elements.find_elements(By.CLASS_NAME,"CBY8yVfV0he1Zbv9Zwjx")
    locations = elements.find_elements(By.CLASS_NAME,"eKDwirBf1zBn7I5MGAOb")
    with open('yc_companies.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for i in range(len(companies)):
            #splits text into list of entries
            entries = (companies[i]).text.split('\n')[1:]
            ahrefs = (companies[i]).get_attribute('href')
            hyperlinks = format_hyperlink(ahrefs)
            entries.insert(0, hyperlinks)
            entries.insert(0, (locations[i]).text)
            entries.insert(0, (names[i]).text)
            writer.writerow(entries)

            