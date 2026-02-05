from appium import webdriver
from appium.options.android import UiAutomator2Options
import sys

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

print("--- Starting Appium Connection Test ---")

options = UiAutomator2Options()
options.platform_name = "Android"
options.automation_name = "UiAutomator2"
options.device_name = "Android Emulator"

print("Options configured. Connecting to http://localhost:4723...")

try:
    driver = webdriver.Remote("http://localhost:4723", options=options)
    print("SUCCESS: Connected to Appium!")
    print(f"Session ID: {driver.session_id}")
    driver.quit()
    print("Driver quit successfully.")
except Exception as e:
    print(f"FAILURE: Could not connect to Appium.")
    print(f"Error Type: {type(e).__name__}")
    print(f"Error Message: {str(e)}")
print("--- Test Completed ---")
