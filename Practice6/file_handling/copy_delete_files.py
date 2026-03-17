# # copy file and back up
import os
import shutil

cur_dir = os.path.dirname(__file__)
data_path = os.path.join(cur_dir, "sample_data.txt")

# shutil.copy(data_path, r"C:\Users\Daniyal\Python\Practice6\file_handling\sample_data1.txt")

# now we can delete this file
# Important! We should use safe method for deleting:
ndata_path = os.path.join(cur_dir, "sample_data1.txt")

if os.path.exists(ndata_path):
    os.remove(ndata_path)
else:
    print("The file does not exist")