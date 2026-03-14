import os

# create nested directories
os.makedirs("test_folder/sub_folder", exist_ok=True)
print("Directories created.\n")

# list files and folders
print("Files and folders in current directory:\n")
for item in os.listdir("."):
    print(item)

# Find files by extension (.txt files)

print("\nSearching for .txt files in directories:")

for root, dirs, files in os.walk("."):
    # os.walk goes through all folders and subfolders
    for file in files:
        # check if the file ends with .txt
        if file.endswith(".txt"):
            # print the full path of the file
            print("TXT file found:", os.path.join(root, file))