from adb_client import ADBController
import sys

def test_adb():
    print("Initializing ADB Controller...")
    controller = ADBController()
    success, msg = controller.connect_device()
    print(f"Connection Result: {success}")
    print(f"Message: {msg}")

    if success:
        print("Attempting screenshot...")
        screenshot = controller.take_screenshot()
        if screenshot:
            print("Screenshot successful (base64 length):", len(screenshot))
        else:
            print("Screenshot failed.")
    else:
        print("Skipping screenshot test due to connection failure.")

if __name__ == "__main__":
    test_adb()
