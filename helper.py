import file_syncer

def getAddedLocalFiles(oldFilenames, newFilenames):
    addedFiles = []
    for filename in newFilenames:
        if filename not in oldFilenames:
            addedFiles.append(filename)
    return addedFiles

def getRemovedLocalFiles(oldFilenames, newFilenames):
    pass
