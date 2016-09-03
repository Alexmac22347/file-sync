import os
from subprocess import call

PARTIALPATHTOREMOTE = '/run/user/1000/gvfs/'


def getRemoteFileNames(directory):
    # Extra stuff to get the path to the phone.
    # It's a different path every time the phone is plugged in

    fullPathToRemote = _getFullPathToRemote(directory)

    return getLocalFileNames(fullPathToRemote)


def getLocalFileNames(directory):
    files = set()
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            files.add(dirpath[len(directory):] + "/" + filename)

    return files


def copyToRemote(fileList, localDirectory, remoteDirectory):
    for filename in fileList:
        fullRemotePath = _getFullPathToRemote(remoteDirectory + filename)
        fullLocalPath = localDirectory + filename
        print "gvfs-copy {} {}".format(fullLocalPath, fullRemotePath)


def deleteFromRemote(fileList, remoteDirectory):
    for filename in fileList:
        fullRemotePath = _getFullPathToRemote(remoteDirectory + filename)
        print "gvfs-rm {}".format(fullRemotePath)


def copyToLocal(fileList, remoteDirectory, localDirectory):
    for filename in fileList:
        fullLocalPath = localDirectory + filename
        fullRemotePath = _getFullPathToRemote(remoteDirectory + filename) 
        print "gvfs-copy {} {}".format(fullRemotePath, fullLocalPath)


def deleteFromLocal(fileList, localDirectory):
    for filename in fileList:
        fullLocalPath = localDirectory + filename
        print "gvfs-rm {}".format(fullLocalPath)

def _getFullPathToRemote(finalPath):
    deviceNames = os.listdir(PARTIALPATHTOREMOTE)
    if not _isSingleDeviceAvailable():
        print "Error getting single device"
        exit()

    return PARTIALPATHTOREMOTE + deviceNames[0] + finalPath


def _isSingleDeviceAvailable():
    if len(os.listdir(PARTIALPATHTOREMOTE)) == 1:
        return True
    return False
