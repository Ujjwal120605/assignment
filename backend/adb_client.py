import adbutils
from adbutils import AdbClient, AdbError
import os
import subprocess
import base64
import shutil

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
            
            self.device = devices[0] # Pick the first device
            return True, f"Connected to {self.device.serial}"
        except Exception as e:
            return False, f"Error connecting to device: {str(e)}"

    def take_screenshot(self):
        if not self.device:
            return None
        try:
            # Get screenshot as PIL Image
            image = self.device.screenshot()
            
            # Save to temporary buffer to get base64
            from io import BytesIO
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            return img_str
        except Exception as e:
            print(f"Screenshot failed: {e}")
            return None

    def tap(self, x, y):
        if not self.device: return
        self.device.click(x, y)

    def type_text(self, text):
        if not self.device: return
        # Create a basic implementation using shell input text
        # Escape spaces and special chars if needed
        escaped_text = text.replace(" ", "%s")
        self.device.shell(f"input text '{escaped_text}'")

    def home(self):
        if not self.device: return
        self.device.keyevent("HOME")

    def back(self):
        if not self.device: return
        self.device.keyevent("BACK")

    def shell(self, cmd):
        if not self.device: return None
        return self.device.shell(cmd)
