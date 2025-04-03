import os
import re
from constants import *
# Get the current working directory
current_dir = os.getcwd()

# Specify the path to the Tests folder
tests_folder = os.path.join(current_dir, 'Tests')

# Get all files in the Tests folder
try:
    files = [f for f in os.listdir(tests_folder) if os.path.isfile(os.path.join(tests_folder, f))]
    for file in files:
        with open(os.path.join(tests_folder, file), 'r') as f:
            content = f.read()
            new_content = re.sub(r"\.\ (?=[a-zA-Z0-9])", "\n", content)
        with open(os.path.join(tests_folder, "Split_" + file), 'w') as f:
            f.write(new_content)
except FileNotFoundError:
    print("Tests folder not found!")