import os
import sys
import config

args = set(sys.argv[1:])
directoriesToList = list(filter(lambda x: x[0] != "-", args)) or ["."]
depth = 1
sortBy = "fileType"
exclude = []
showAll = False

for arg in args:
    splitted = arg.split("=")

    if splitted[0] in ["-a", "--all"]:
        showAll = True

    if splitted[0] in ["-t", "--tree"]:
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

    if splitted[0] in ["-x", "--exclude"]:
        exclude = splitted[1].split(",")
        exclude = list(map(lambda ext: ext.strip(), exclude))

def ToFullPath(path):
    result = path

    " If it's not a full path, convert it "
    if result[0] != "/":
        result = os.getcwd() + "/" + (path if path != "." else "")

    " If it doesn't end with a '/', add it "
    if result[-1] != "/":
        result += "/"

    return result

def PrintItem(extension, itemName, indent=0):
    prepend = config.COLORS["GREY"] + " " * (indent - 2) + "|-- "

    if indent <= 2:
        prepend = " " * indent

    # Print Standart Style if Not Defined
    type = extension if extension in config.STYLES else "FILE"

    # Prepend Color and Icon
    prepend += config.COLORS[config.STYLES[type][1]]
    prepend += config.STYLES[type][0]

    if extension and extension not in ["FILE", "FOLDER"]:
        itemName = ".".join(itemName.split(".")[:-1]) + config.COLORS["GREY"] + "." + extension

    print(prepend, itemName)

def PrintDirectory(path, indent, depth):
    path = ToFullPath(path)
    items = os.listdir(path)

    if not showAll:
        items = filter(lambda item: (item[0] != "."), items)

    folders = []
    files = []

    for item in items:
        if config.HideNodeModules and item == "node_modules":
            continue

        if os.path.isdir(path + item):
            folders.append(item)
        else:
            files.append(item)

    for folder in sorted(folders):
        PrintItem("FOLDER", folder, indent)

        if depth > 0:
            PrintDirectory(path + folder, indent + 2, depth - 1)

    # Sort by File Type or Name
    if sortBy == "name":
        files.sort()
    else:
        files.sort(key=lambda item: (item.split(".")[-1], item))

    # Print Files
    for file in files:
        extension = file.split(".")[-1] if "." in file else ""

        if extension in exclude and not showAll:
            continue

        PrintItem(extension, file, indent)

for directory in directoriesToList:
    if depth < 1:
        break

    if not os.path.isdir(directory):
        continue

    # If listing multiple directories, print directory names
    if len(directoriesToList) > 1:
        print(config.COLORS["GREY"], directory)

    PrintDirectory(directory, 2, depth-1)
