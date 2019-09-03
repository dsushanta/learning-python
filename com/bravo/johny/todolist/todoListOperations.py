import os


def lineCountInAFile(fileName):
    file = open(fileName, 'r')
    count = 0
    line = file.readline()
    while line:
        count += 1
        line = file.readline()
    file.close()

    return count


def createToDoList(fileName):
    open(fileName, 'w+').close()


def showToDoList(fileName):
    file = open(fileName, 'r')
    line = file.readline()
    count = 0
    while line:
        count += 1
        print(count, "-", line)
        line = file.readline()
    file.close()


def getFileContentAsAList(fileName):
    file = open(fileName, 'r')
    list_lines = []
    line = file.readline()
    while line:
        list_lines.append(line)
        line = file.readline()
    file.close()
    return list_lines


def getLineFromAFileFromLineNumber(fileName, lineNumber):
    searched_line = ''
    file = open(fileName, 'r')
    count = 0
    line = file.readline()
    while line:
        count += 1
        if lineNumber == count:
            searched_line = line
            break
        line = file.readline()
    file.close()
    return searched_line


def removeAnEntry(fileName, entryNumber):
    count = lineCountInAFile(fileName)
    if entryNumber < 1 or entryNumber > count:
        print("\nInvalid entry number.")
    else:
        entry_to_be_removed = getLineFromAFileFromLineNumber(fileName, entryNumber)
        line_list = getFileContentAsAList(fileName)
        line_list.sort()
        line_list.remove(entry_to_be_removed)
        open(fileName, 'w').close()
        file = open(fileName, 'a')
        for line in line_list:
            file.writelines(line)
        print('Following entry has been removed :', entry_to_be_removed)
        file.close()


def addAnEntry(fileName, entry):
    file = open(fileName, 'a')
    file.writelines(entry)
    file.writelines("\n")
    file.close()


def deleteToDoList(fileName):
    os.remove(fileName)
