# Read and print file contents

file_name = "sample.txt"

try:
    with open(file_name, "r") as f:
        print("File content:\n")
        for line in f:
            print(line.strip())
except FileNotFoundError:
    print("File does not exist.")