from pathlib import Path
import os
from datetime import datetime
import re
import shutil
import sys
import time


class Instruction:
    def __init__(self, line):
        [extensions, output_dir] = re.split("=>", line, 2)
        extensions = re.sub(r"[\[\]\s]", "", extensions)
        self.extensions = re.split(",", extensions)
        self.output_dir = output_dir.strip()

    def get_extensions(self):
        return self.extensions

    def get_output_dir(self):
        return self.output_dir


instructions = {}

download_path = ""
settings_path = "settings/settings.txt"

time_filter = 0
dir = os.listdir()
logs = []

if "logs" not in dir:
    os.mkdir("logs")

log_time = datetime.now()
log_path = "logs/{}_{}.txt".format(len(os.listdir("logs")), log_time.date())

if "settings" not in dir:
    os.mkdir("settings")
if not os.path.exists(settings_path):
    with open(settings_path, "w") as sf:
        sf.write("# Lines beginning with \"#\" are ignored\n")
        sf.write("# Enter the path to your downloads folder on the line \
below:\n")
        sf.write(str(Path.home() / "Downloads"))
        sf.write("\n")
        sf.write("# Ignore files newer than:\n0\n# minutes old\n")
        sf.write("# Edit the lines below, or add more using the same format. \
\n")
        sf.write("# All the files in the downloads folder with filename \
extensions matching the\n")
        sf.write("# ones inside the square brackets are moved to the \
directory specified after \"=>\"\n")
        sf.write(r"[jpg, png] => {}".format(str(Path.home() / "Pictures")))
        logs.append("Created file settings/settings.txt\n")
        logs.append("Edit the settings file to set up the filetype rules to \
your liking.\n")

with open(settings_path, "r") as sf:
    lines = []
    for line in sf:
        if line != "" and line[0] != "#":
            lines.append(line.strip())

    # The first line in the settings file should be the downloads folder
    download_path = lines[0].strip()
    # The second line should be the time filter (in minutes)
    if len(sys.argv) <= 1 or sys.argv[1] not in ["anytime", "notime", "at"]:
        time_filter = int(lines[1], base=10)
    for line in lines:
        # All lines not starting with a list of file extensions are not needed
        if len(line) > 0 and line[0] == "[":
            instruction = Instruction(line)
            for extension in instruction.get_extensions():
                if extension not in instructions.keys():
                    instructions[extension] = instruction.get_output_dir()
                    if not os.path.exists(instruction.get_output_dir()):
                        path = Path(instruction.get_output_dir())
                        path.mkdir(parents=True)

if len(instructions.keys()) < 1:
    print("No instructions found in \"settings/settings.txt\"")
    quit()


if download_path != "":
    if os.path.exists(download_path):
        downloads_files = os.listdir(download_path)
        for d in downloads_files:
            extension = d.split(".")[-1]
            if extension in instructions.keys():
                old_filename = os.path.join(download_path, d)
                if os.path.getmtime(old_filename) + (time_filter * 60) < time.time():
                    new_filename = os.path.join(instructions[extension], d)
                    while os.path.isfile(new_filename):
                        new_filename_parts = new_filename.split(".")
                        new_filename = ".".join(new_filename_parts[0:-1])
                        new_filename += "_copy." + new_filename_parts[-1]
                    # If the destination and origin are on the same drive
                    if old_filename.split(":")[0] == new_filename.split(":")[0]:
                        os.rename("{}".format(old_filename), "{}"
                                  .format(new_filename))
                    # If the destination and origin are on different drives
                    else:
                        shutil.move(old_filename, new_filename)
                    logs.append("{} => {}".format(d, instructions[extension]))
    else:
        logs.append("The paths found in {} do not exist! Exiting..."
            .format(settings_path))
else:
    logs.append("Open the file \"settings/settings.txt\" and enter the paths \
to your downloads folder and your target folder")

if len(logs) > 0:
    with open(log_path, "a") as log_file:
        log_file.write("Logs for program run on {}:\n".format(log_time))
        for line in logs:
            log_file.write("{}\n".format(line))

quit()
