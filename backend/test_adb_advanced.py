from adb_client import ADBController
import time

def test_controller():
    controller = ADBController()
    success, msg = controller.connect_device()
    print(f"Connection Status: {success} - {msg}")
    
    if not success:
        return

    print("\n--- Testing Screen Dump ---")
    start_time = time.time()
    elements = controller.dump_screen()
    end_time = time.time()
    print(f"Dumped {len(elements)} elements in {end_time - start_time:.2f} seconds.")
    
    if elements:
        print("First 3 elements:")
        for el in elements[:3]:
            print(el)
            
    print("\n--- Testing Find Element ---")
    # Try to find common elements likely to be on screen or home screen
    targets = ["ChatGPT", "Settings", "Phone", "Camera", "Search"]
    for t in targets:
        el = controller.find_actionable_element(t)
        if el:
            print(f"Found '{t}': {el['center']}")
        else:
            print(f"'{t}' not found.")

if __name__ == "__main__":
    test_controller()
