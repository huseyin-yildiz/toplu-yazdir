# Name   : Toplu-Yazdir
# Author : Huseyin Yildiz
# Date   : 18.10.2023

# Uncomment this chdir line for pyinstaller build
#os.chdir(sys._MEIPASS)
from gui import *


root.mainloop()

try:
    # Delete temp files
    os.remove(MERGED_PATH)
    os.remove(BACK_COVER_PATH)
    os.remove(FRONT_COVER_PATH)

except OSError:
    pass