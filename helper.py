def getAddedFiles(oldFilenames, newFilenames):
    addedFiles = set()
    for filename in newFilenames:
        if filename not in oldFilenames:
            addedFiles.add(filename)
    return addedFiles


def getRemovedFiles(oldFilenames, newFilenames):
    removedFiles = set()
    for filename in oldFilenames:
        if filename not in newFilenames:
            removedFiles.add(filename)
    return removedFiles


def writeConfigFilesToDisk(localFiles, remoteFiles, config):
    config.values['files']['local'] = ""
    config.values['files']['remote'] = ""

    for filename in localFiles:
        config.values['files']['local'] += filename + '\n'
    for filename in remoteFiles:
        config.values['files']['remote'] += filename + '\n'

    config.writeConfig()


def appendFilesToConfig(localFiles, remoteFiles, config):
    # This is needed. I'm confused.
    config.values['files']['local'] += '\n'
    config.values['files']['remote'] += '\n'

    for filename in localFiles:
        config.values['files']['local'] += filename + '\n'
    for filename in remoteFiles:
        config.values['files']['remote'] += filename + '\n'


def removeFilesFromConfig(localFiles, remoteFiles, config):
    for filename in localFiles:
        config.values['files']['local'] = config.values['files']['local'].replace(filename + '\n', "")
    for filename in remoteFiles:
        config.values['files']['remote'] = config.values['files']['remote'].replace(filename + '\n', "")


def addFilesToCache(localFiles, remoteFiles, selectedFiles):
    localFiles.update(
        set(selectedFiles))
    remoteFiles.update(
        set(selectedFiles))


def removeFilesFromCache(localFiles, remoteFiles, selectedFiles):
    localFiles.difference_update(
        set(selectedFiles))
    remoteFiles.difference_update(
        set(selectedFiles))

            
def escapeString(string):
    escapeCharacters = [
            ",",
            "?",
            "[",
            "]",
            " ",
            "!",
            "(",
            ")"
            ]

    returnString = string

    for char in escapeCharacters:
        returnString = returnString.replace(char, "\\" + char)

    return returnString
