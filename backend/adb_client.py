import adbutils
from adbutils import AdbClient, AdbError
import os
import shutil
import base64
import time
from xml_parser import XMLParser

class ADBController:
    def __init__(self, host="127.0.0.1", port=5037):
        if not shutil.which("adb"):
            # Try common locations
            common_paths = [
                os.path.expanduser("~/Library/Android/sdk/platform-tools/adb"),
                "/opt/homebrew/bin/adb",
                "/usr/local/bin/adb"
            ]
            for p in common_paths:
                if os.path.exists(p):
                    os.environ["PATH"] += os.pathsep + os.path.dirname(p)
                    break

        try:
            self.client = AdbClient(host=host, port=port)
        except Exception as e:
            print(f"Failed to connect to ADB server: {e}")
            self.client = None
        self.device = None

    def connect_device(self):
        if not self.client:
            return False, "ADB Client not initialized"
        
        try:
            devices = self.client.device_list()
            if not devices:
                return False, "No devices connected"
            
            # Prioritize real devices (exclude emulators)
            target_device = devices[0]
            for d in devices:
                if not d.serial.startswith("emulator-"):
                    target_device = d
                    break
            
            self.device = target_device
            return True, f"Connected to {self.device.serial}"
        except Exception as e:
            return False, f"Error connecting to device: {str(e)}"

    def dump_screen(self):
        """Dumps user UI xml and returns parsed elements."""
        if not self.device: return []
        try:
            # Dump XML to sdcard
            self.device.shell("uiautomator dump /sdcard/window_dump.xml")
            # Pull to memory (string)
            xml_content = self.device.sync.read_text("/sdcard/window_dump.xml")
            
            # DEBUG: Print XML stats
            print(f"DEBUG: XML Content Length: {len(xml_content)}")
            print(f"DEBUG: XML Snippet: {xml_content[:100]}")
            
            parser = XMLParser(xml_content)
            elements = parser.find_elements()
            print(f"DEBUG: Parsed {len(elements)} elements")
            return elements
        except Exception as e:
            print(f"Error dumping screen: {e}")
            return []

    def find_actionable_element(self, text):
        """Finds an element by text and returns its center coordinates."""
        elements = self.dump_screen()
        for el in elements:
            # Check text or content-desc
            if (text.lower() in el['text'].lower()) or (text.lower() in el['content_desc'].lower()):
                return el
        return None

    def tap_element(self, text):
        """Finds element by text and taps it."""
        el = self.find_actionable_element(text)
        if el:
            x, y = el['center']
            print(f"Tapping '{text}' at ({x}, {y})")
            self.tap(x, y)
            return True
        print(f"Element '{text}' not found.")
        return False

    def tap(self, x, y):
        if not self.device: return
        self.device.click(x, y)

    def type_text(self, text):
        if not self.device: return
        # Escape spaces and special chars
        escaped_text = text.replace(" ", "%s").replace("'", r"\'")
        self.device.shell(f"input text '{escaped_text}'")

    def press_enter(self):
        if not self.device: return
        self.device.keyevent("66") # ENTER

    def home(self):
        if not self.device: return
        self.device.keyevent("HOME")

    def back(self):
        if not self.device: return
        self.device.keyevent("BACK")

    def open_app(self, package_name):
        if not self.device: return
        # Using monkey is often easier than finding the specific activity
        self.device.shell(f"monkey -p {package_name} -c android.intent.category.LAUNCHER 1")
