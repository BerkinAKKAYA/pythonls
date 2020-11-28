import os
import sys
import colors
import icons

args = sys.argv[1:]
directoriesToList = []
depth = 1

for arg in args:
    if arg[0] != "-" and os.path.isdir(arg):
        directoriesToList.append(arg)

    splitted = arg.split("=")
    if splitted[0] == "--tree":
        depth = int(splitted[1])

directoriesToList = directoriesToList or ["."]

def ToFullPath(path):
    result = path

    " If it's not a full path, convert it "
    if result[0] != "/":
        result = os.getcwd() + "/" + (path if path != "." else "")

    " If it doesn't end with a '/', add it "
    if result[-1] != "/":
        result += "/"

    return result

def PrintItem(itemType, itemName, indent=0):
    prepend = colors.GREY + " " * (indent - 2) + "|-- "

    if indent <= 2:
        prepend = " " * indent

    if itemType == "FOLDER":
        prepend += colors.BLUE2 + icons.FOLDER
    if itemType == "FILE":
        prepend += colors.GREEN2 + icons.FILE
    if itemType == "VIDEO":
        prepend += colors.RED2 + icons.VIDEO
    if itemType == "PHOTO":
        prepend += colors.YELLOW2 + icons.PHOTO

    print(prepend, itemName)

def PrintDirectory(path, indent=0, depth=1):
    path = ToFullPath(path)

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
        if os.path.isdir(path + item):
            folders.append(item)
            continue

        # Find out the extension
        extension = item.split(".")[-1] if "." in item[1:] else ""

        if extension in ["mkv", "mp4", "webm"]:
            files["VIDEO"].append(item)
        elif extension in ["jpg", "jpeg", "png"]:
            files["PHOTO"].append(item)
        else:
            files["FILE"].append(item)

    for folder in sorted(folders):
        PrintItem("FOLDER", folder, indent)
        
        if depth > 0:
            PrintDirectory(path + folder, indent + 2, depth - 1)

    for fileType in files:
        files[fileType].sort()

        for f in files[fileType]:
            PrintItem(fileType, f, indent)

for directory in directoriesToList:
    if depth < 1:
        break

    " If listing multiple directories, print directory names "
    if len(directoriesToList) > 1:
        print(colors.GREY, directory)

    PrintDirectory(directory, 2, depth-1)
