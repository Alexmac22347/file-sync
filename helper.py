def getAddedFiles(oldFilenames, newFilenames):
    """Returns a set containing files which are in newFilenames,
    but not in oldFilenames"""

    addedFiles = set()
    for filename in newFilenames:
        if filename not in oldFilenames:
            addedFiles.add(filename)
    return addedFiles


def getRemovedFiles(oldFilenames, newFilenames):
    """Returns a set containing files which are not in newFilenames,
    but in oldFilenames"""

    removedFiles = set()
    for filename in oldFilenames:
        if filename not in newFilenames:
            removedFiles.add(filename)
    return removedFiles


def writeConfigFilesToDisk(localFiles, remoteFiles, config):
    """writes config.ini using localFiles and remoteFiles.

    Note: The "settings" field of config is retained. The
    "files" field is replaced with localFiles and remoteFiles

    Args:
        localFiles: set containing all the local filenames
        remoteFiles: set containing all the remote filenames
        config: the config which will be used to write the config.ini file

    Returns:
        Nothing

    """

    config.values['files']['local'] = ""
    config.values['files']['remote'] = ""

    for filename in localFiles:
        config.values['files']['local'] += filename + '\n'
    for filename in remoteFiles:
        config.values['files']['remote'] += filename + '\n'

    config.writeConfig()


def appendFilesToConfig(localFiles, remoteFiles, config):
    """Appends localFiles and remoteFiles to config."""

    # This is needed. I'm confused.
    config.values['files']['local'] += '\n'
    config.values['files']['remote'] += '\n'

    for filename in localFiles:
        config.values['files']['local'] += filename + '\n'
    for filename in remoteFiles:
        config.values['files']['remote'] += filename + '\n'


def removeFilesFromConfig(localFiles, remoteFiles, config):
    """Deletes filenames contained in localFiles and remoteFiles
    from config"""

    for filename in localFiles:
        config.values['files']['local'] = config.values['files']['local'].replace(filename + '\n', "")
    for filename in remoteFiles:
        config.values['files']['remote'] = config.values['files']['remote'].replace(filename + '\n', "")


def addFilesToCache(localFiles, remoteFiles, selectedFiles):
    """Adds selectedFiles to sets localFiles and remoteFiles"""

    localFiles.update(
        set(selectedFiles))
    remoteFiles.update(
        set(selectedFiles))


def removeFilesFromCache(localFiles, remoteFiles, selectedFiles):
    """Removes selectedFiles from sets localFiles and remoteFiles"""

    localFiles.difference_update(
        set(selectedFiles))
    remoteFiles.difference_update(
        set(selectedFiles))


def escapeString(string):
    """Returns string with escaped characters

    For example, if string is "Hello, world!",
    then "Hello\,\ world\!" will be returned

    """

    escapeCharacters = [
            ",",
            "?",
            "[",
            "]",
            " ",
            "!",
            "(",
            ")",
            "'",
            "\u2013"
            ]

    returnString = string

    for char in escapeCharacters:
        returnString = returnString.replace(char, "\\" + char)

    return returnString
