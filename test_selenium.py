from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# 1. Path to the Browser
firefox_path = "/usr/lib/firefox/firefox" 

# 2. Path to the Driver (CHANGE THIS LINE)
# We moved it to 'local/bin', so we must tell Python that!
driver_path = "/usr/local/bin/geckodriver"

service = Service(executable_path=driver_path)
options = Options()
options.binary_location = firefox_path

try:
    print(f"Launching Browser: {firefox_path}")
    print(f"Using Driver:    {driver_path}")

    driver = webdriver.Firefox(service=service, options=options)
    
    driver.get("https://google.com")
    print("\nSUCCESS: It works!")
    print("Page Title:", driver.title)
    driver.quit()

except Exception as e:
    print("\nERROR:")
    print(e)