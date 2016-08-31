import os

PARTIALPATHTOREMOTE = '/run/user/1000/gvfs/'


def isSingleDeviceAvailable():
    if len(os.listdir(PARTIALPATHTOREMOTE)) == 1:
        return True
    return False


def getRemoteFileNames(directory):
    # Extra stuff to get the path to the phone.
    # It's a different path every time the phone is plugged in
    deviceNames = os.listdir(PARTIALPATHTOREMOTE)
    if not isSingleDeviceAvailable():
        print "Error getting single device"
        exit()

    # TODO: Do this with os module
    fullPathToRemote = PARTIALPATHTOREMOTE + deviceNames[0] + directory

    return getLocalFileNames(fullPathToRemote)


def getLocalFileNames(directory):
    files = set()
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            files.add(dirpath[len(directory):] + "/" + filename)

    return files


def copyToRemote(fileList, localDirectory, remoteDirectory):
    pass


def deleteFromRemote(fileList, localDirectory, remoteDirectory):
    pass


def copyToLocal(fileList, remoteDirectory, localDirectory):
    pass


def deleteFromLocal(fileList, remoteDirectory, localDirectory):
    pass
