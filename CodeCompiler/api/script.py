import subprocess
import platform
import sys

def check_tool(tool_name, command, success_message="Success"):
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"{tool_name}: {success_message}")
        else:
            print(f"{tool_name}: Failed with return code {result.returncode}")
    except FileNotFoundError:
        print(f"{tool_name}: Not installed or not in PATH.")
    except subprocess.TimeoutExpired:
        print(f"{tool_name}: Command timed out.")
    except Exception as e:
        print(f"{tool_name}: Error occurred - {str(e)}")

def main():
    # Check Python
    check_tool("Python", [sys.executable, "-c", "print('Hello, Python!')"], "Python is installed and working")

    # Check Node.js
    check_tool("Node.js", ["node", "-e", "console.log('Hello, Node.js!')"], "Node.js is installed and working")

    # Check Bash
    if platform.system() != "Windows":
        check_tool("Bash", ["bash", "-c", "echo 'Hello, Bash!'"], "Bash is installed and working")
    else:
        print("Bash: Skipping check on Windows unless WSL is used.")

    # Check SQLite3
    check_tool("SQLite3", ["sqlite3", "-version"], "SQLite3 is installed and working")

    # Add checks for other tools here

if __name__ == "__main__":
    main()