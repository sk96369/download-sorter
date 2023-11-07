# Moves all the .gif, .mp4 and .webm files from the downloads folder to the desired
# target folder

from pathlib import Path
import os
from datetime import datetime
import re

download_path = ""
target_path = ""
settings_path = "settings/settings.txt"
dir = os.listdir()

if "logs" not in dir:
    os.mkdir("logs")

log_time = datetime.now()
log_path = "logs/{}_{}.txt".format(len(os.listdir("logs")), log_time.date())
with open(log_path, "w") as l:
    l.write("Logs for program run on {}:".format(log_time))

if "settings" not in dir:
    os.mkdir("settings")
if not os.path.exists(settings_path):
    with open(settings_path, "w") as sf:
        sf.write("# Lines beginning with \"#\" are ignored\n")
        sf.write("#Enter the path to your downloads folder on the line below:\n")
        sf.write("\n")
        sf.write("#Enter the path to your target folder on the line below:\n")
        sf.write("\n")

with open(settings_path, "r") as sf:
    with open(log_path, "a") as l:
        l.write("Reading paths from {}\n".format(settings_path))
    for line in sf:
        if line[0] != "#":
            if download_path == "":
                download_path = line.strip()
                if download_path[-1] != "/":
                        download_path += "/"
            else:
                if target_path == "":
                    target_path = line.strip()
                    if target_path[-1] != "/":
                        target_path += "/"

filecount = 0
if download_path != "" and target_path != "":
    if os.path.exists(download_path) and os.path.exists(target_path):
        downloads_files = os.listdir(download_path)
        file_pattern = re.compile(".(gif|mp4|webm)$")
        for d in downloads_files:
            matches = re.search(file_pattern, d)
            if matches:
                filecount += 1
                os.rename("{}{}".format(download_path, d), "{}{}".format(target_path, d))
    else:
        with open(log_path, "a") as l:
            l.write("The paths found in {} do not exist! Exiting...".format(settings_path))
else:
    with open(log_path, "a") as l:
        l.write("Open the file \"settings/settings.txt\" and enter the paths to your downloads folder and your target folder")

with open(log_path, "a") as l:
    l.write("Moved {} files of filetypes .gif, .webm and .mp4 from\n{}\nto\n{}.\n".format(filecount, download_path, target_path))

quit()
