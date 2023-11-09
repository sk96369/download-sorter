from pathlib import Path
import os
from datetime import datetime
import re


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
        sf.write("# Enter the path to your downloads folder on the line \
below:\n")
        sf.write(str(Path.home() / "Downloads"))
        sf.write("\n")
        sf.write("# Edit the lines below, or add more using the same format. \
\n")
        sf.write("# All the files in the downloads folder with filename \
extensions matching the\n")
        sf.write("# ones inside the square brackets are moved to the \
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

logs = []

if download_path != "":
    if os.path.exists(download_path):
        downloads_files = os.listdir(download_path)
        for d in downloads_files:
            extension = d.split(".")[-1]
            if extension in instructions.keys():
                os.rename("{}".format(os.path.join(download_path, d)), "{}"
                          .format(os.path.join(instructions[extension], d)))
                logs.append("{} => {}".format(d, instructions[extension]))
    else:
        with open(log_path, "a") as log_file:
            log_file.write("The paths found in {} do not exist! Exiting..."
                    .format(settings_path))
else:
    with open(log_path, "a") as log_file:
        log_file.write("Open the file \"settings/settings.txt\" and enter the paths \
to your downloads folder and your target folder")

if len(logs) > 0:
    with open(log_path, "a") as log_file:
        log_file.write("Logs for program run on {}:\n".format(log_time))
        for line in logs:
            log_file.write("{line}\n")

quit()
