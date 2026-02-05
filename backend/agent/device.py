from appium import webdriver
from appium.options.android import UiAutomator2Options

import shutil
import subprocess

def get_driver():
    # 1. Check if ADB is installed
    adb_path = shutil.which("adb")
    if not adb_path:
        print("[Device] ADB binary not found in PATH.")
        return None

    # 2. Check for connected devices
    try:
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
        if "device\n" not in result.stdout and "emulator" not in result.stdout:
            print("[Device] ADB installed, but no device/emulator connected.")
            return None
    except Exception as e:
        print(f"[Device] Failed to run 'adb devices': {e}")
        return None

    # 3. Attempt Appium Connection
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    # Using a generic device name, Appium usually picks the first available if not specific
    options.device_name = "Android Emulator" 
    
    try:
        # Appium 2.x defaults to / instead of /wd/hub
        driver = webdriver.Remote(
            "http://localhost:4723",
            options=options
        )
        return driver
    except Exception as e:
        print(f"[Device] Appium connection failed: {e}")
        return None
