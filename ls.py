import os
import sys
import colors
import icons

args = sys.argv[1:]

def PrintItem(itemType, itemName, indent=0):
    prepend = " " * indent

    if itemType == "FOLDER":
        prepend += colors.RED2 + icons.FOLDER
    if itemType == "FILE":
        prepend += colors.BLUE2 + icons.FILE
    if itemType == "VIDEO":
        prepend += colors.BLUE2 + icons.VIDEO
    if itemType == "PHOTO":
        prepend += colors.BLUE2 + icons.PHOTO

    print(prepend, itemName)

def PrintDirectory(path):
    folders = []
    files = {
        "VIDEO": [],
        "PHOTO": [],
        "FILE": []
    }

    for item in os.listdir(path):
        # Hide dotfiles if -a is not in args
        if item[0] == "." and "-a" not in args:
            continue
        
        # Print as FOLDER and continue if it's a folder
        if os.path.isdir(item):
            folders.append(item)
            continue

        # Find out the extension
        extension = item.split(".")[-1] if "." in item[1:] else ""

        # If there is no extension, print as FILE and continue
        if not extension:
            files["FILE"].append(["FILE", item])
            continue

        # If there is an extension, print with correct icon and color
        if extension in ["mkv", "mp4", "webm"]:
            files["VIDEO"].append(item)
        if extension in ["jpg", "jpeg", "png"]:
            files["PHOTO"].append(item)

    for folder in sorted(folders):
        PrintItem("FOLDER", folder)

    for fileType in files:
        files[fileType].sort()

        for f in files[fileType]:
            PrintItem(fileType, f)

PrintDirectory(".")
