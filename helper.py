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


def updateAndWriteConfigAddedFiles(localAddedFiles, remoteAddedFiles, config):
    for filename in set.intersection(localAddedFiles, remoteAddedFiles):
        config.values['files']['local'] += filename + '\n'
        config.values['files']['remote'] += filename + '\n'

    config.writeConfig()


def updateAndWriteConfigRemovedFiles(localRemovedFiles, remoteRemovedFiles, config):
    for filename in set.intersection(localRemovedFiles, remoteRemovedFiles):
        config.values['files']['local'] = config.values['files']['local'].replace(filename + '\n', "")
        config.values['files']['remote'] = config.values['files']['remote'].replace(filename + '\n', "")

    config.writeConfig()
