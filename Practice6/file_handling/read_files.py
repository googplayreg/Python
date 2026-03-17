# reading and printing file's text
import os

cur_dir = os.path.dirname(__file__)
data_dir = os.path.join(cur_dir, "sample_data.txt")

with open(data_dir, "r") as f:
    print(f.read())