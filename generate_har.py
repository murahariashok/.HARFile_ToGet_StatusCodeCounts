import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    """Setup Chrome WebDriver with DevTools Protocol enabled."""
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--auto-open-devtools-for-tabs")
    chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})  # Use set_capability for logging prefs

    service = Service(executable_path="chromedriver.exe")  # Replace with your chromedriver path
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def save_har_file(driver, har_file_path):
    """Capture network logs and save them as a .har file."""
    logs = driver.get_log("performance")
    events = [json.loads(entry["message"])["message"] for entry in logs]
    network_logs = [event for event in events if "Network.responseReceived" in event["method"]]

    # Convert to HAR format
    har = {
        "log": {
            "version": "1.2",
            "creator": {"name": "Selenium HAR Generator", "version": "1.0"},
            "entries": network_logs,
        }
    }
    with open(har_file_path, "w") as har_file:
        json.dump(har, har_file, indent=4)

def main_Testcase():
    driver = setup_driver()
    driver.get("https://exactspace.co")

    # Wait for the page to load, specify a page element to wait for
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1")))  # Change the tag name based on your page

    # Save HAR file
    har_file_path = "exactspace.har"
    save_har_file(driver, har_file_path)
    print(f"HAR file saved as {har_file_path}")

    # Analyze HAR file
    # analyze_har_file(har_file_path)

    # Close the browser
    driver.quit()

if __name__ == "__main__":
    main_Testcase()


