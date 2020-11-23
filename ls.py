import os
import sys
import colors
import icons

args = sys.argv[1:]
files = os.listdir('.')
indent = " " * 2

if "-a" not in args:
    files = [f for f in files if f[0] != "."]

files.sort()

for f in files:
    fullPath = os.getcwd() + "/" + f
    isFolder = os.path.isdir(fullPath)

    if isFolder:
        print(indent + colors.BLUE + icons.FOLDER + f)
    else:
        print(indent + colors.RED + icons.FILE + f)
