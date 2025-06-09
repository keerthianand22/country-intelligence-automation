import os
import subprocess

# Define the path to your "IP code" folder
folder_path = os.path.expanduser("~/Desktop/IP code")

# List all .py files in the folder (excluding this script)
scripts = [f for f in os.listdir(folder_path) if f.endswith(".py") and f != "run_scripts.py"]

if not scripts:
    print("No Python scripts found in the folder.")
    exit()

# Run each script sequentially
for script in scripts:
    script_path = os.path.join(folder_path, script)
    print(f"Running {script}...")

    result = subprocess.run(["python3", script_path], capture_output=True, text=True)

    # Print output and error messages
    print(result.stdout)
    if result.stderr:
        print(f"Error in {script}:\n{result.stderr}")
        exit(1)

print("All scripts executed successfully!")
