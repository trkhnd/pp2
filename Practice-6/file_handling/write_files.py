# Create a file and append new lines

file_name = "sample.txt"

# create and write
with open(file_name, "w") as f:
    f.write("Hello\n")
    f.write("Python file handling\n")
    f.write("Practice 6\n")

print("File created and data written.\n")

# append
with open(file_name, "a") as f:
    f.write("This line was appended\n")

print("New line appended.\n")

# verify
with open(file_name, "r") as f:
    print("Updated file content:\n")
    print(f.read())