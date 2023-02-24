from selenium import webdriver

# create a new Chrome browser instance
driver = webdriver.Chrome()

# navigate to the Google website
driver.get("https://www.google.com")

# close the browser window
driver.quit()
