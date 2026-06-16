import re
import os

def check_services():
    services_file = "services/all_services.py"
    if not os.path.exists(services_file):
        print(f"Error: {services_file} not found!")
        return

    with open(services_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Find all class definitions
    classes = re.split(r'\n(?=class\s+\w+)', content)
    
    # We want to find classes that have session calls without timeout
    no_timeout_classes = []
    direct_requests_classes = []
    
    for cls in classes:
        lines = cls.split('\n')
        if not lines:
            continue
        
        # Get class name
        class_match = re.match(r'class\s+(\w+)', lines[0])
        if not class_match:
            continue
        class_name = class_match.group(1)
        
        # Check for direct requests library calls instead of self.session
        if "requests.get(" in cls or "requests.post(" in cls:
            direct_requests_classes.append(class_name)
            
        # Check for session calls
        session_calls = re.findall(r'self\.session\.(get|post|put|delete|request)\((.*?)\)', cls, re.DOTALL)
        for method, args in session_calls:
            # Check if timeout is in args
            if "timeout=" not in args:
                no_timeout_classes.append((class_name, method, args.strip().split('\n')[0]))

    print(f"=== CHECK RESULTS FOR {services_file} ===")
    
    if direct_requests_classes:
        print(f"\n[WARNING] Found {len(direct_requests_classes)} classes using direct 'requests.*' instead of 'self.session.*':")
        for c in direct_requests_classes:
            print(f"  - {c}")
    else:
        print("\n[OK] No classes are using direct 'requests.*' calls.")
        
    if no_timeout_classes:
        print(f"\n[WARNING] Found {len(no_timeout_classes)} session calls missing 'timeout=':")
        for c, method, snippet in no_timeout_classes:
            print(f"  - {c}.{method}: {snippet}...")
    else:
        print("\n[OK] All session calls specify 'timeout='.")

if __name__ == "__main__":
    check_services()
