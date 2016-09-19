import Tkinter as tk


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
            "'"
            ]

    returnString = string

    for char in escapeCharacters:
        returnString = returnString.replace(char, "\\" + char)

    return returnString

def promptUserForDirectories():
    popup = tk.Tk()
    popup.resizable(width=False, height=False)
    popup.geometry('270x100')
    popup.grid()

    label = tk.Label(popup, text="Enter Remote and Local Directories:")
    label.grid(row=0,column=0,columnspan=2,sticky='W')

    localDirectoryText = tk.StringVar()
    remoteDirectoryText = tk.StringVar()

    # Create the Local and Remote labels
    localLabel = tk.Label(
        text="Local:")
    remoteLabel = tk.Label(
        text="Remote:")

    localDirectoryBox = tk.Entry(width=25,
        textvariable=localDirectoryText)
    remoteDirectoryBox = tk.Entry(width=25,
        textvariable=remoteDirectoryText)

    localLabel.grid(row=1, column=0, sticky='W')
    remoteLabel.grid(row=2, column=0, sticky='W')
    localDirectoryBox.grid(row=1, column=1, sticky='EW')
    remoteDirectoryBox.grid(row=2, column=1, sticky='EW')

    # Create the cancel and save buttons
    exitButton = tk.Button(popup, width=10, text="Exit", command = exit)
    exitButton.place(x=20,y=65)
    saveButton = tk.Button(popup, width=10, text="Save", command = popup.destroy)
    saveButton.place(x=150,y=65)

    popup.mainloop()
    return (localDirectoryText.get(), remoteDirectoryText.get())
