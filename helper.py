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


def writeDuplicateAddedFiles(addedFiles, config):
    # This is needed. I'm confused.
    config.values['files']['local'] += '\n'
    config.values['files']['remote'] += '\n'

    for filename in addedFiles:
        config.values['files']['local'] += filename + '\n'
        config.values['files']['remote'] += filename + '\n'

    config.writeConfig()


def writeDuplicateRemovedFiles(removedFiles, config):
    for filename in removedFiles:
        config.values['files']['local'] = config.values['files']['local'].replace(filename + '\n', "")
        config.values['files']['remote'] = config.values['files']['remote'].replace(filename + '\n', "")

    config.writeConfig()
