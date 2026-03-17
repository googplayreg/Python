# adding some text in the existing file
import os

cur_dir = os.path.dirname(__file__)
data_dir = os.path.join(cur_dir, "sample_data.txt")

x = input("Write in the file: ")
with open(data_dir, "a") as f:
    f.write(f" {x}")

with open(data_dir) as f:
    print(f.read())