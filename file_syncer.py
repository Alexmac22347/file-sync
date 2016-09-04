import os
from subprocess import call
import helper

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
        fullEscapedRemotePath = helper.escapeString(fullRemotePath)
        fullLocalPath = localDirectory + filename
        fullEscapedRemotePathLocalPath = helper.escapeString(fullLocalPath)

        remotePath = os.path.split(fullRemotePath)[0]

        if not os.path.exists(remotePath):
            os.mkdir(remotePath)

        print "gvfs-copy {} {}".format(fullEscapedRemotePathLocalPath, fullEscapedRemotePath)
        call("gvfs-copy " + fullEscapedRemotePathLocalPath + " " + fullEscapedRemotePath, shell=True)


def deleteFromRemote(fileList, remoteDirectory):
    for filename in fileList:
        fullRemotePath = _getFullPathToRemote(remoteDirectory + filename)
        fullEscapedRemotePath = helper.escapeString(fullRemotePath)

        print "gvfs-rm {}".format(fullEscapedRemotePath)
        call("gvfs-rm " + fullEscapedRemotePath, shell=True)

        remotePath = os.path.split(fullRemotePath)[0]
        print "Hey " + remotePath

        if(len(os.listdir(remotePath)) == 0):
            os.rmdir(remotePath)


def copyToLocal(fileList, remoteDirectory, localDirectory):
    for filename in fileList:
        fullLocalPath = localDirectory + filename
        fullEscapedLocalPath = helper.escapeString(fullLocalPath)
        fullRemotePath = _getFullPathToRemote(remoteDirectory + filename)
        fullEscapedRemotePath = helper.escapeString(fullRemotePath)

        localPath = os.path.split(fullLocalPath)[0]

        if not os.path.exists(localPath):
            os.mkdir(localPath)

        print "gvfs-copy {} {}".format(fullEscapedRemotePath, fullEscapedLocalPath)
        call("gvfs-copy " + fullEscapedRemotePath + " " + fullEscapedLocalPath, shell=True)


def deleteFromLocal(fileList, localDirectory):
    for filename in fileList:
        fullLocalPath = localDirectory + filename
        fullEscapedLocalPath = helper.escapeString(fullLocalPath)

        print "gvfs-rm {}".format(fullEscapedLocalPath)
        call("gvfs-rm " + fullEscapedLocalPath, shell=True)

        localPath = os.path.split(fullLocalPath)[0]

        if(len(os.listdir(localPath)) == 0):
            os.rmdir(localPath)


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
