"""This module is used to access files and folders on disk. It can also
access an mtp device"""

import os
from subprocess import call
import helper

PARTIALPATHTOREMOTE = '/run/user/1000/gvfs/'


def getRemoteFileNames(directory):
    """Returns a set containing all the filenames in directory.
    directory should be located on an MTP device.
    the filenames also include part of the path to that file, starting
    from director.

    Eg. if directory was /Card/Music/, and there was a file 
    /Card/Music/Songs/song.mp3, then the filename /Songs/song.mp3
    will be in the set which is returned

    """

    # Extra stuff to get the path to the phone.
    # It's a different path every time the phone is plugged in
    fullPathToRemote = _getFullPathToRemote(directory)

    return getLocalFileNames(fullPathToRemote)


def getLocalFileNames(directory):
    """Returns a set containing all the filenames in directory.
    the filenames also include part of the path to that file, starting
    from director.

    Eg. if directory was /home/alex/Music/, and there was a file 
    /home/alex/Music/Songs/song.mp3, then the filename /Songs/song.mp3
    will be in the set which is returned

    """

    files = set()
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            files.add(dirpath[len(directory):] + "/" + filename)

    return files


def copyToRemote(fileList, localDirectory, remoteDirectory):
    """Copies all the files in fileList from localDirectory to 
    remoteDirectory, where remoteDirectory is located on an MTP device"""

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
    """Deletes all the files in fileList from remoteDirectory.
    remoteDirectory should be located on an MTP device.
    This will also remove any leftover empty folders"""

    for filename in fileList:
        fullRemotePath = _getFullPathToRemote(remoteDirectory + filename)
        fullEscapedRemotePath = helper.escapeString(fullRemotePath)

        print "gvfs-rm {}".format(fullEscapedRemotePath)
        call("gvfs-rm " + fullEscapedRemotePath, shell=True)

        # Delete empty folder:
        remotePath = os.path.split(fullRemotePath)[0]
        if(len(os.listdir(remotePath)) == 0):
            os.rmdir(remotePath)


def copyToLocal(fileList, remoteDirectory, localDirectory):
    """Copies all files in fileList from remoteDirectory to 
    localDirectory. remoteDirectory should be located on an MTP
    device"""

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
    """Deletes all the files in fileList from localDirectory.
    This will also remove any leftover empty folders"""

    for filename in fileList:
        fullLocalPath = localDirectory + filename
        fullEscapedLocalPath = helper.escapeString(fullLocalPath)

        print "gvfs-rm {}".format(fullEscapedLocalPath)
        call("gvfs-rm " + fullEscapedLocalPath, shell=True)

        localPath = os.path.split(fullLocalPath)[0]

        if(len(os.listdir(localPath)) == 0):
            os.rmdir(localPath)


def _getFullPathToRemote(finalPath):
    """Returns the full path to a location on a remote device.
    
    Eg. if finalPath is /Card/Music/, a string like
    "/run/user/1000/gvfs/mtp:20AC2009/Card/Music/"
    will be returned

    This will throw an exception if a single MTP device is
    not found. So if more than one MTP device is plugged it, or no
    MTP device is plugged in, and exception is thrown

    """

    deviceNames = os.listdir(PARTIALPATHTOREMOTE)
    if not _isSingleDeviceAvailable():
        print "Error getting single MTP Device"
        exit()

    return PARTIALPATHTOREMOTE + deviceNames[0] + finalPath


def _isSingleDeviceAvailable():
    """Returns true if and only if ONE MTP device is plugged in"""

    if len(os.listdir(PARTIALPATHTOREMOTE)) == 1:
        return True
    return False
