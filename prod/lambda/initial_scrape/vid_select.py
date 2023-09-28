import subprocess
import os
from os import path
import random

#Get list of videos
files = os.walk("""/Volumes/NO NAME/DA FOLDER""")
file_list = []
for p,s,f in files:
    for name in f:
        file_list.append(os.path.join(p,name))

#CLean up list
file_list=[x.replace('._','') for x in file_list]
file_list = list(set(file_list))

# Randomly select 10 videos
random_vids = random.sample(file_list,1)

# Open videos
for vid in random_vids:
    subprocess.Popen(["open",vid])
    os.wait()