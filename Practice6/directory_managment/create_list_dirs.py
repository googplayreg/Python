import os
from pathlib import Path

# nested directories
tpath = r"C:\Users\Daniyal\Python\Practice6\directory_managment\test1\test2\test3.txt"
os.makedirs(tpath, exist_ok = True)

# listing folders and files
folder_path = Path(r"C:\Users\Daniyal\Python\Practice6\directory_managment")

for item in folder_path.iterdir():
    if item.is_dir():
        print(f"This is a folder: {item.name}")
    elif item.is_file():
        print(f"This ia a file: {item.name}")

# finding files by extension
print("\nThe following python files are found:")
for path in Path(r"C:\Users\Daniyal\Python\Practice6\directory_managment").glob("*.py"):
    print(path.name)