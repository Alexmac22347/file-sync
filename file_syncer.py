import config
import selection_state
import helper
import disk_interface


class file_syncer:

    def __init__(self):
        self.gconfig = config.config()
        self.gconfig.values['files'] = {}
        self.gconfig.values['settings'] = {}

        self.cachedLocalFiles = set()
        self.cachedRemoteFiles = set()
        self.latestLocalFiles = set()
        self.latestRemoteFiles = set()

        # Try to read from the config file. create it if it does not exist
        try:
            self.gconfig.readConfig()
            self.cachedLocalFiles = set(self.gconfig.values['files']['local'].split('\n'))
            self.cachedRemoteFiles = set(self.gconfig.values['files']['remote'].split('\n'))

            self.latestLocalFiles = disk_interface.getLocalFileNames(self.gconfig.values['settings']['local'])
            self.latestRemoteFiles = disk_interface.getRemoteFileNames(self.gconfig.values['settings']['remote'])

        except config.NoConfigException:
            print "Initializing configuration file"
            self.gconfig.values['settings']['local'] = '/home/alex/Music/'
            self.gconfig.values['settings']['remote'] = '/Card/Music/'

            self.cachedLocalFiles = disk_interface.getLocalFileNames(self.gconfig.values['settings']['local'])
            self.cachedRemoteFiles = disk_interface.getRemoteFileNames(self.gconfig.values['settings']['remote'])

            self.latestLocalFiles = self.cachedLocalFiles.copy()
            self.latestRemoteFiles = self.cachedRemoteFiles.copy()

            helper.writeConfigFilesToDisk(self.cachedLocalFiles, self.cachedRemoteFiles, self.gconfig)

        self.addedToLocal = helper.getAddedFiles(
            self.cachedLocalFiles,
            self.latestLocalFiles)
        self.removedFromLocal = helper.getRemovedFiles(
            self.cachedLocalFiles,
            self.latestLocalFiles)
        self.addedToRemote = helper.getAddedFiles(
            self.cachedRemoteFiles,
            self.latestRemoteFiles)
        self.removedFromRemote = helper.getRemovedFiles(
            self.cachedRemoteFiles,
            self.latestRemoteFiles)

        # If a file is added to the local AND the remote directories, we update
        # the config file, and update the data structures to reflect this.
        # Same goes for files deleted locally AND remotely
        commonAddedFiles = set.intersection(self.addedToLocal, self.addedToRemote)
        commonRemovedFiles = set.intersection(self.removedFromLocal, self.removedFromRemote)

        helper.appendFilesToConfig(commonAddedFiles, commonAddedFiles, self.gconfig)
        helper.removeFilesFromConfig(commonRemovedFiles, commonRemovedFiles, self.gconfig)

        self.addedToLocal.difference_update(commonAddedFiles)
        self.addedToRemote.difference_update(commonAddedFiles)

        self.removedFromLocal.difference_update(commonRemovedFiles)
        self.removedFromRemote.difference_update(commonRemovedFiles)

        # If a file is added to the local directory, but it already exists in
        # the remote directory, and already appears under the "remote" section
        # of config.ini, we can simply add it to the "local" section of config.ini
        # without asking the user. In a way, it's already been "copied" to remote.
        # Same goes for other cases
        addedLocallyButExistsInRemote = set.intersection(self.addedToLocal, self.latestRemoteFiles)
        removedLocallyButDoesntExistInRemote = self.removedFromLocal - self.latestRemoteFiles
        addedRemotelyButExistsInLocal = set.intersection(self.addedToRemote, self.latestLocalFiles)
        removedRemotelyButDoesntExistInLocal = self.removedFromRemote - self.latestLocalFiles

        # Update the config
        helper.appendFilesToConfig(addedLocallyButExistsInRemote, addedRemotelyButExistsInLocal, self.gconfig)
        helper.removeFilesFromConfig(removedLocallyButDoesntExistInRemote, removedRemotelyButDoesntExistInLocal, self.gconfig)

        # Update our data
        self.addedToLocal.symmetric_difference_update(addedLocallyButExistsInRemote)
        self.removedFromLocal.symmetric_difference_update(removedLocallyButDoesntExistInRemote)
        self.addedToRemote.symmetric_difference_update(addedRemotelyButExistsInLocal)
        self.removedFromRemote.symmetric_difference_update(removedRemotelyButDoesntExistInLocal)

        self.gconfig.writeConfig()

    def onUpdateButtonClick(self, state, selectedFiles):

        if state == selection_state.AddToRemote:
            disk_interface.copyToRemote(selectedFiles,
                                     self.gconfig.values['settings']['local'],
                                     self.gconfig.values['settings']['remote'])

            helper.addFilesToCache(self.cachedLocalFiles, self.cachedRemoteFiles, selectedFiles)

        elif state == selection_state.RemoveFromRemote:
            disk_interface.deleteFromRemote(selectedFiles,
                                         self.gconfig.values['settings']['remote'])

            helper.removeFilesFromCache(self.cachedLocalFiles, self.cachedRemoteFiles, selectedFiles)

        elif state == selection_state.AddToLocal:
            disk_interface.copyToLocal(selectedFiles,
                                    self.gconfig.values['settings']['remote'],
                                    self.gconfig.values['settings']['local'])

            helper.addFilesToCache(self.cachedLocalFiles, self.cachedRemoteFiles, selectedFiles)

        elif state == selection_state.RemoveFromLocal:
            disk_interface.deleteFromLocal(selectedFiles,
                                        self.gconfig.values['settings']['local'])

            helper.removeFilesFromCache(self.cachedLocalFiles, self.cachedRemoteFiles, selectedFiles)

        # Remember to write config to disk before exiting
        # Maybe we should write this each time we switch states
        helper.writeConfigFilesToDisk(self.cachedLocalFiles, self.cachedRemoteFiles, self.gconfig)

# This is a global file syncer made available to other modules
globalFileSyncer = file_syncer()
