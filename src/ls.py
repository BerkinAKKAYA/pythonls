import os
import sys
import styles

args = set(sys.argv[1:])
directoriesToList = list(filter(lambda x: x[0] != "-", args)) or ["."]
depth = 1
sortBy = "fileType"

for arg in args:
    splitted = arg.split("=")

    if splitted[0] == "--tree":
        depth = int(splitted[1])

    if splitted[0] in ["-h", "--help"]:
        depth = 0
        print("""
            pythonls by Berkin AKKAYA

            -h      Show Help
            --tree  Show Directory Tree
            --name  Sort By Name
        """)

    if splitted[0] in ["-n", "--name"]:
        sortBy = "name"

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
    prepend = styles.COLORS["GREY"] + " " * (indent - 2) + "|-- "

    if indent <= 2:
        prepend = " " * indent

    if itemType in styles.STYLES:
        # Color
        prepend += styles.COLORS[styles.STYLES[itemType][1]]
        # Name
        prepend += styles.STYLES[itemType][0]

    print(prepend, itemName)

def PrintDirectory(path, indent=0, depth=1):
    path = ToFullPath(path)

    folders = []
    files = {
        "VIDEO": [],
        "PHOTO": [],
        "FILE": [],
        "AUDIO": [],
        "HTML": [],
        "CSS": [],
        "JS": [],
        "JSON": [],
        "PDF": [],
        "SRT": [],
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
        elif extension in ["mp3", "waw"]:
            files["AUDIO"].append(item)
        elif extension in ["html"]:
            files["HTML"].append(item)
        elif extension in ["css", "sass", "scss"]:
            files["CSS"].append(item)
        elif extension in ["js"]:
            files["JS"].append(item)
        elif extension in ["pdf"]:
            files["PDF"].append(item)
        elif extension in ["srt"]:
            files["SRT"].append(item)
        else:
            files["FILE"].append(item)

    for folder in sorted(folders):
        PrintItem("FOLDER", folder, indent)

        if depth > 0:
            PrintDirectory(path + folder, indent + 2, depth - 1)

    for fileType in files:
        files[fileType].sort()

    if sortBy == "fileType":
        for fileType in files:
            for file in files[fileType]:
                PrintItem(fileType, file, indent)
    if sortBy == "name":
        allFiles = []
        for fileType in files:
            for file in files[fileType]:
                allFiles.append([file, fileType])

        allFiles.sort()

        for file in allFiles:
            PrintItem(file[1], file[0], indent)

for directory in directoriesToList:
    if depth < 1:
        break

    if not os.path.isdir(directory):
        continue

    " If listing multiple directories, print directory names "
    if len(directoriesToList) > 1:
        print(styles.COLORS["GREY"], directory)

    PrintDirectory(directory, 2, depth-1)
