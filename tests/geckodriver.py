from selenium import webdriver

# create a new Firefox browser instance
driver = webdriver.Firefox()

# navigate to the Google website
driver.get("https://www.firefox.com")

# close the browser window
driver.quit()
