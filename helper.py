def getAddedFiles(oldFilenames, newFilenames):
    addedFiles = set()
    for filename in newFilenames:
        if filename not in oldFilenames:
            addedFiles.append(filename)
    return addedFiles

def getRemovedFiles(oldFilenames, newFilenames):
    removedFiles = set()
    for filename in oldFilenames:
        if filename not in newFilenames:
            removedFiles.append(filename)
    return removedFiles

def writeConfigFilesToDisk(localFiles, remoteFiles, config):
    config.values['files']['local'] = ""
    config.values['files']['remote'] = ""
    for filename in localFiles:
        config.values['files']['local'] += filename + "\n"
    for filename in remoteFiles:
        config.values['files']['remote'] += filename + "\n"

    config.writeConfig()
