"""
<div jsname="o6bZLc"><input type="hidden" name="entry.220378635" value="joe"><input type="hidden" name="entry.2066858529" value=""><input type="hidden" name="entry.30071131" value="Yes"><input type="hidden" name="entry.2120341158" value="[[[&quot;1f6HDc5qGhUj0HkkS9lcJyhcQR3xzE7lA&quot;,&quot;Durbak_20250116_GRB250116A.csv&quot;,&quot;text/csv&quot;]]]"><input type="hidden" name="emailAddress" value="jmdurbak@terpmail.umd.edu"><input type="hidden" name="dlut" value="1742938172361"></div>
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

# Set up WebDriver
driver = webdriver.Chrome(ChromeDriverManager().install())

# Open the Google Form URL
form_url = 'https://your-google-form-url'
driver.get(form_url)

# Allow the page to load completely
time.sleep(3)

# Fill out the form (example: finding input fields and filling them)
input_field_1 = driver.find_element(By.XPATH, '//input[@aria-label="Your Field Label"]')
input_field_1.send_keys("Some text")

# Locate the file upload field (find the input type="file" tag)
file_upload_field = driver.find_element(By.XPATH, '//input[@type="file"]')

# Upload the file
file_upload_field.send_keys('/path/to/your/file')  # Use the path to the file you want to upload

# Optionally, click the submit button (if you know its XPath)
submit_button = driver.find_element(By.XPATH, '//span[text()="Submit"]/ancestor::button')
submit_button.click()

# Wait for the form to submit
time.sleep(5)

# Close the browser
driver.quit()



