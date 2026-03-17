import shutil
from pathlib import Path

src = Path(r"C:\Users\Daniyal\Python\Practice6\README.md")
dst = Path(r"C:\Users\Daniyal\Python\Practice6\directory_managment\README.md")

# copying file
shutil.copy2(src, dst)

# replacing file
# shutil.move(src, dst)