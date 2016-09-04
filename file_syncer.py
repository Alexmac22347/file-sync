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
        fullRemotePath = helper.escapeString(fullRemotePath)
        fullLocalPath = localDirectory + filename
        fullLocalPath = helper.escapeString(fullLocalPath)
        print "gvfs-copy {} {}".format(fullLocalPath, fullRemotePath)
        call("gvfs-copy " + fullLocalPath + " " + fullRemotePath, shell=True)


def deleteFromRemote(fileList, remoteDirectory):
    for filename in fileList:
        fullRemotePath = _getFullPathToRemote(remoteDirectory + filename)
        fullRemotePath = helper.escapeString(fullRemotePath)
        print "gvfs-rm {}".format(fullRemotePath)
        call("gvfs-rm " + fullRemotePath, shell=True)


def copyToLocal(fileList, remoteDirectory, localDirectory):
    for filename in fileList:
        fullLocalPath = localDirectory + filename
        fullLocalPath = helper.escapeString(fullLocalPath)
        fullRemotePath = _getFullPathToRemote(remoteDirectory + filename) 
        fullRemotePath = helper.escapeString(fullRemotePath)
        print "gvfs-copy {} {}".format(fullRemotePath, fullLocalPath)
        call("gvfs-copy " + fullRemotePath + " " + fullLocalPath, shell=True)


def deleteFromLocal(fileList, localDirectory):
    for filename in fileList:
        fullLocalPath = localDirectory + filename
        fullLocalPath = helper.escapeString(fullLocalPath)
        print "gvfs-rm {}".format(fullLocalPath)
        call("gvfs-rm " + fullLocalPath, shell=True)

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
