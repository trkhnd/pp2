import shutil
import os

source = "sample.txt"
destination = "test_folder/sample.txt"

# move file
if os.path.exists(source):
    shutil.move(source, destination)
    print("File moved successfully.")
else:
    print("Source file not found.")