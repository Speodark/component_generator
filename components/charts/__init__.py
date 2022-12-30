import glob
import os
import sys

# Get the path to the current directory
current_dir = os.path.dirname(__file__)

# Add the path to the current directory to the Python search path
sys.path.append(current_dir)

# Create an empty dictionary to store the file names and class objects
charts_dict = {}

# Get a list of all the Python files in the current directory
files = glob.glob(os.path.join(current_dir, '*.py'))
ready_files = [
    'bar'
]
# Loop through the files and import everything from each file
for file in files:
    # Get the name of the file, without the .py extension
    file_name = os.path.splitext(os.path.basename(file))[0]
    if file_name == '__init__':
        continue
    if file_name not in ready_files:
        continue
    with open(file) as f:
        exec(f.read())

    # Convert the file name to CamelCase
    class_name = ''.join(word.capitalize() for word in file_name.split('_'))
    # Get the class object from the imported module
    cls = eval(class_name)
    # Add the file name and class object to the dictionary
    charts_dict[file_name.capitalize()] = cls
