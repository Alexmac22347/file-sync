import os

PARTIALPATHTOREMOTE = '/run/user/1000/gvfs/'

# TODO: Determine what to do if there is more than one device


def isDeviceAvailable():
    if len(os.listdir(PARTIALPATHTOREMOTE)) == 0:
        return False
    return True


def getRemoteFileNames(directory):
    # Extra stuff to get the path to the phone.
    # It's a different path every time the phone is plugged in
    deviceNames = os.listdir(PARTIALPATHTOREMOTE)
    if len(deviceNames) != 1:
        print "Error getting single device"
        return

    fullPathToRemote = os.path.join(PARTIALPATHTOREMOTE, deviceNames[0], directory)

    return getLocalFileNames(fullPathToRemote)

def getLocalFileNames(directory):
    files = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if dirpath + filename not in files:
                files.append(dirpath[len(directory):] + "/" + filename)

    return files


def copyToRemote():
    pass


def copyToLocal():
    pass


def deleteFromRemote():
    pass


def deleteFromLocal():
    pass

for filename in getRemoteFileNames('Card/Music/Songs/'):
    print filename
