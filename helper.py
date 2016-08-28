def getAddedFiles(oldFilenames, newFilenames):
    addedFiles = []
    for filename in newFilenames:
        if filename not in oldFilenames:
            addedFiles.append(filename)
    return addedFiles

def getRemovedFiles(oldFilenames, newFilenames):
    removedFiles = []
    for filename in oldFilenames:
        if filename not in newFilenames:
            removedFiles.append(filename)
    return removedFiles
