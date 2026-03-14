import shutil
import os

source = "sample.txt"
backup = "backup_sample.txt"

# copy file
shutil.copy(source, backup)
print("File copied successfully.")

# delete file safely
if os.path.exists(backup):
    os.remove(backup)
    print("Backup file deleted.")
else:
    print("Backup file not found.")