from pathlib import Path
import os
from datetime import datetime
import re


class Instruction:
    def __init__(self, extensions, output_dir):
        extensions = re.sub(r"[\[\]\s]", "", extensions)
        self.extensions = re.split(",", extensions)
        self.output_dir = "output_dir"


filetypes = ".(mov|gif|mp4|webm|gif)$"

download_path = ""
target_path = ""
instructions = []
settings_path = "settings/settings.txt"
dir = os.listdir()

if "logs" not in dir:
    os.mkdir("logs")

log_time = datetime.now()
log_path = "logs/{}_{}.txt".format(len(os.listdir("logs")), log_time.date())

if "settings" not in dir:
    os.mkdir("settings")
if not os.path.exists(settings_path):
    with open(settings_path, "w") as sf:
        sf.write("# Lines beginning with \"#\" are ignored\n")
        sf.write("# Enter the path to your downloads folder on the line\
                below:\n")
        sf.write("\n")
        sf.write("# Edit the lines below, or add more using the same format.\
                \n")
        sf.write("# All the files in the downloads folder with filename\
                 extensions matching the\n")
        sf.write("# ones inside the square brackets are moved to the\
                directory specified after \"=>\"\n")
        sf.write(r"[jpg, png] => C:\Users\You\Pictures\ ")

with open(settings_path, "r") as sf:
    lines = []
    for line in sf:
        if line[0] != "#":
            lines.append(line.strip())

    # The first line in the settings file should be the downloads folder
    download_path = lines[0].strip()
    for line in lines:
        # All lines not starting with a list of file extensions are not needed
        if line[0] == "[":
            

            if download_path == "":
                download_path = line.strip()
                if download_path[-1] != "/":
                        download_path += "/"
            elif target_path == "":
                target_path = line.strip()
                if target_path[-1] != "/":
                    target_path += "/"
            elif secondary_path == "":
                secondary_path = line.strip()
                if secondary_path[-1] != "/":
                    secondary_path += "/"

filecount = 0
secondary_filecount = 0
if download_path != "" and target_path != "":
    if os.path.exists(download_path) and os.path.exists(target_path):
        downloads_files = os.listdir(download_path)
        file_pattern_1 = re.compile(filetypes)
        for d in downloads_files:
            matches = re.search(file_pattern_1, d)
            if matches:
                filecount += 1
                os.rename("{}{}".format(download_path, d), "{}{}".format(target_path, d))
        if secondary_path != "" and secondary_filetypes != "":
            file_pattern_2 = re.compile(secondary_filetypes)
            for d in downloads_files:
                matches = re.search(file_pattern_2, d)
                if matches:
                    secondary_filecount += 1
                    os.rename("{}{}".format(download_path, d), "{}{}".format(secondary_path, d))

    else:
        with open(log_path, "a") as l:
            l.write("The paths found in {} do not exist! Exiting...".format(settings_path))
else:
    with open(log_path, "a") as l:
        l.write("Open the file \"settings/settings.txt\" and enter the paths to your downloads folder and your target folder")

if filecount > 0 or secondary_filecount > 0:
    with open(log_path, "a") as l:
        l.write("Logs for program run on {}:\n".format(log_time))
        l.write("Moved {} files of filetypes .gif, .webm, .mov and .mp4 from\n{}\nto\n{}.\n".format(filecount,     download_path, target_path))
        l.write("Moved {} files of filetypes .png, .jpg and .jpeg from\n{}\nto\n{}.\n".format(filecount, download_path, secondary_path))


quit()
