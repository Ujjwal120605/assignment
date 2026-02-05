from agent.device import get_driver

ALLOWED_ACTIONS = {"open_app", "authenticate_if_needed", "type", "submit", "extract_result"}

def execute(steps):
    driver = get_driver()
    
    if not driver:
        # Improved Simulated Execution Mode
        print(">>> Running in SIMULATION MODE (No device detected) <<<")
        results = []
        for step in steps:
            action = step.get('action')
            if action not in ALLOWED_ACTIONS:
                print(f"Skipping invalid action: {action}")
                continue
                
            details = step.get('text') or step.get('app') or ""
            print(f"  [SIMULATED] {action}: {details}")
            results.append(f"{action} ({details})")
            
        return f"Simulation Mode: Executed {len(results)} steps. Actions: " + ", ".join(results)

    try:
        execution_log = []
        for step in steps:
            action = step.get('action')
            print(f"[Real Device Mode] Executing: {action}")
            
            if action == 'open_app':
                app_name = step.get('app')
                # 1. Fuzzy find package
                # This requires ADB shell access. We can use the driver or subprocess.
                # Using subprocess for "adb shell pm list packages" is easier.
                pkg = _find_package(app_name)
                if pkg:
                    print(f"  -> Found package: {pkg}")
                    driver.activate_app(pkg)
                    execution_log.append(f"Opened {app_name} ({pkg})")
                else:
                    print(f"  -> App {app_name} not found")
                    execution_log.append(f"Failed to open {app_name} (Not Installed)")

            elif action == 'type':
                text = step.get('text')
                # Use ADB input text for generic typing (escaped)
                # This works if the field is focused.
                # Ideally we check for an EditText, but for the demo input injection is robust.
                _adb_type(text)
                execution_log.append(f"Typed: {text}")

            elif action == 'submit':
                driver.press_keycode(66) # ENTER
                execution_log.append("Pressed Enter")
            
            elif action == 'authenticate_if_needed':
                # Placeholder for auth logic
                pass
            
            elif action == 'extract_result':
                # Placeholder
                pass

        return "Real Device execution completed. Steps: " + ", ".join(execution_log)
    except Exception as e:
        return f"Execution failed: {str(e)}"
    finally:
        if driver:
            driver.quit()

def _find_package(app_name):
    import subprocess
    try:
        # Get list of packages
        res = subprocess.run(["adb", "shell", "pm", "list", "packages"], capture_output=True, text=True)
        packages = [line.replace("package:", "").strip() for line in res.stdout.splitlines()]
        
        # Simple fuzzy match: check if app_name (lowercase) is in package name
        query = app_name.lower().replace(" ", "")
        for pkg in packages:
            if query in pkg:
                return pkg
        return None
    except:
        return None

def _adb_type(text):
    import subprocess
    # ADB input text requires spaces to be %s
    escaped = text.replace(" ", "%s").replace("'", "").replace('"', "")
    subprocess.run(["adb", "shell", "input", "text", escaped])
