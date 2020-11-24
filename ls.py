# TODO: Add the option to accept multiple folders as input

import os
import sys
import colors
import icons

args = sys.argv[1:]
filesAndFolders = os.listdir('.')
indent = " " * 2

for folderName in [x for x in args if x[0] != "-"]:
    print(folderName)
    filesAndFolders = os.listdir(folderName)

# Hide dotfiles if "-a" flag is not passed
if "-a" not in args:
    filesAndFolders = [f for f in filesAndFolders if f[0] != "."]

files = []
folders = []

for f in filesAndFolders:
    fullPath = os.getcwd() + "/" + f
    isFolder = os.path.isdir(fullPath)

    if isFolder:
        folders.append(f)
    else:
        files.append(f)

for folderName in folders:
    print(indent + colors.BLUE + icons.FOLDER + folderName)

for fileName in files:
    print(indent + colors.RED + icons.FILE + fileName)
