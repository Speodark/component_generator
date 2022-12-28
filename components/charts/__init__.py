import glob

# Create an empty dictionary to store the file names and class objects
charts_dict = {}

# Get a list of all the Python files in the current directory
files = glob.glob('*.py')
# Loop through the files and import everything from each file
for file in files:
    if file == '__init__.py':
        continue
    with open(file) as f:
        exec(f.read())

    # Get the name of the file, without the .py extension
    file_name = file[:-3]

    # Convert the file name to CamelCase
    class_name = ''.join(word.capitalize() for word in file_name.split('_'))

    # Get the class object from the imported module
    cls = eval(class_name)
    # Add the file name and class object to the dictionary
    charts_dict[file_name] = cls
