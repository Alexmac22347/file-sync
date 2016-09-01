import Tkinter as tk
import config
import file_syncer
import helper

WINHEIGHT = 445
WINWIDTH = 296

# Use a global config class
# Changes to this object are seen in every class
gconfig = config.globalConfig
gconfig.values['files'] = {}
gconfig.values['settings'] = {}

# sets which contain filenames
# of "tracked" files
localFiles = set()
remoteFiles = set()
latestLocalFiles = set() 
latestRemoteFiles = set() 


class gui(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # This thing is not going to be resizable
        self.resizable(width=False, height=False)
        self.geometry('{}x{}'.format(WINWIDTH, WINHEIGHT))

        container = tk.Frame(self)
        container.grid()

        # Read the config file. If it is empty, initialize it 
        global localFiles, remoteFiles, latestLocalFiles, latestRemoteFiles
        try:
            gconfig.readConfig()
            localFiles = set(gconfig.values['files']['local'].split('\n'))
            remoteFiles = set(gconfig.values['files']['remote'].split('\n'))

            latestLocalFiles = file_syncer.getLocalFileNames(
                gconfig.values['settings']['local'])
            latestRemoteFiles = file_syncer.getRemoteFileNames(
                gconfig.values['settings']['remote'])

        except config.NoConfigException:
            print "Initializing configuration file"
            gconfig.values['settings']['local'] = '/home/alex/Music/'
            gconfig.values['settings']['remote'] = '/Card/Music/'

            localFiles = file_syncer.getLocalFileNames(
                gconfig.values['settings']['local'])
            remoteFiles = file_syncer.getRemoteFileNames(
                gconfig.values['settings']['remote'])

            latestLocalFiles = localFiles.copy()
            latestRemoteFiles = remoteFiles.copy()

            helper.writeConfigFilesToDisk(localFiles, remoteFiles, gconfig)

        # This dictionary contains the two Frames,
        # MainPage and SettingsPage
        self.frames = {}
        for F in (MainPage, SettingsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.showFrame(MainPage)

    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.showGUI()


class MainPage(tk.Frame):

    # This is used to represent what part of the program we are in.
    # It will help determine what to do when a button is pressed,
    # and what files to display in the list box
    class State:
        AddToRemote = 1
        RemoveFromRemote = 2
        AddToLocal = 3
        RemoveFromLocal = 4

    def __init__(self, parent, controller):
        self.currentState = self.State.AddToRemote
        tk.Frame.__init__(self, parent)
        self.initializeWidgets(controller)

        self.addedToLocal = helper.getAddedFiles(
                    localFiles,
                    latestLocalFiles)
        self.removedFromLocal = helper.getRemovedFiles(
                    localFiles,
                    latestLocalFiles)
        self.addedToRemote = helper.getAddedFiles(
                    remoteFiles,
                    latestRemoteFiles)
        self.removedFromRemote = helper.getRemovedFiles(
                    remoteFiles,
                    latestRemoteFiles)

        # If a file is added to the local AND the remote directories, we update
        # the config file, and update the data structures to reflect this.
        # Same goes for files deleted locally AND remotely
        commonAddedFiles = set.intersection(self.addedToLocal, self.addedToRemote)
        commonRemovedFiles = set.intersection(self.removedFromLocal, self.removedFromRemote)
        helper.writeDuplicateAddedFiles(commonAddedFiles, gconfig)
        helper.writeDuplicateRemovedFiles(commonRemovedFiles, gconfig)

        self.addedToLocal.difference_update(commonAddedFiles)
        self.addedToRemote.difference_update(commonAddedFiles)

        self.removedFromLocal.difference_update(commonRemovedFiles)
        self.removedFromRemote.difference_update(commonRemovedFiles)


    def initializeWidgets(self, controller):
        # Create the grid layout manager
        self.grid()

        # Create listbox with vertical and horizontal scroll
        # Create the vertical scroll
        self.yScroll = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.yScroll.grid(row=0, column=1, sticky=tk.N + tk.S)
        # Create the horizontal scroll
        self.xScroll = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.xScroll.grid(row=1, column=0, sticky=tk.E + tk.W)
        # Create the listbox
        self.listbox = tk.Listbox(self, activestyle='none',
                                  selectmode='multiple',
                                  height=20,
                                  width=35,
                                  xscrollcommand=self.xScroll.set,
                                  yscrollcommand=self.yScroll.set)
        self.xScroll['command'] = self.listbox.xview
        self.yScroll['command'] = self.listbox.yview

        # Add a settings button
        self.settingsIcon = tk.BitmapImage(file='settings_icon.xbm')
        self.settingsButton = tk.Button(
            self,
            image=self.settingsIcon,
            command=lambda: self.onSettingsButtonClick(controller))

        # Create the "update all" button
        self.updateAllButton = tk.Button(
            self,
            text="Add all to remote",
            command=self.onUpdateAllButtonClick,
            width=28)

        # Create the "update selected" button
        self.updateSelectedButton = tk.Button(
            self, text="Add selected to remote",
            command=self.onUpdateSelectedButtonClick)

        # Create the "skip" button
        self.skipButton = tk.Button(
            self, text="Skip", command=self.onSkipButtonClick)

        # Create the info box
        self.infoBox = tk.Label(
            self, height=2, anchor='w', fg='black', bg='white', relief='ridge', justify=tk.LEFT)

    # This will draw the GUI based on the current state
    def showGUI(self):
        global localFiles, remoteFiles
        # These things here will always be visible
        # no matter what state we're in
        self.listbox.grid(row=0, column=0, sticky='NSEW')
        # Clear the listbox
        self.listbox.delete(0, self.listbox.size())
        self.settingsButton.grid(row=2, column=0, sticky='EN')
        self.updateAllButton.grid(row=2, column=0, sticky='W')
        self.updateSelectedButton.grid(
            row=3, column=0, sticky='EW')
        self.skipButton.grid(row=4, column=0, sticky='EW')
        self.infoBox.grid(row=5, column=0, sticky='EW')

        if self.currentState == self.State.AddToRemote:
            for filename in self.addedToLocal:
                self.listbox.insert(0, filename)

            self.updateAllButton['text']="Add all to remote"
            self.updateSelectedButton['text']="Add selected to remote"
            return

        if self.currentState == self.State.RemoveFromRemote:
            for filename in self.removedFromLocal:
                self.listbox.insert(0, filename)

            self.updateAllButton['text']="Remove all from remote"
            self.updateSelectedButton['text']="Remove selected from remote"
            return

        if self.currentState == self.State.AddToLocal:
            for filename in self.addedToRemote:
                self.listbox.insert(0, filename)

            self.updateAllButton['text']="Add all to local"
            self.updateSelectedButton['text']="Add selected to local"
            return

        if self.currentState == self.State.RemoveFromLocal:
            for filename in self.removedFromRemote:
                self.listbox.insert(0, filename)

            self.updateAllButton['text']="Remove all from local"
            self.updateSelectedButton['text']="Remove selected from local"
            return

    # Various event handlers
    def onSettingsButtonClick(self, controller):
        controller.showFrame(SettingsPage)

    def onUpdateAllButtonClick(self):
        global localFiles, remoteFiles, latestLocalFiles, latestRemoteFiles

        if self.currentState == self.State.AddToRemote:
            file_syncer.copyToRemote(self.listbox.get(0, self.listbox.size()),
                                     gconfig.values['settings']['local'],
                                     gconfig.values['settings']['remote'])

            localFiles.update(set(self.listbox.get(0, self.listbox.size())))
            remoteFiles.update(set(self.listbox.get(0, self.listbox.size())))

            self.currentState=self.State.RemoveFromRemote

        elif self.currentState == self.State.RemoveFromRemote:
            file_syncer.deleteFromRemote(self.listbox.get(0, self.listbox.size()),
                                         gconfig.values['settings']['local'],
                                         gconfig.values['settings']['remote'])

            localFiles.difference_update(
                set(self.listbox.get(0, self.listbox.size())))
            remoteFiles.difference_update(
                set(self.listbox.get(0, self.listbox.size())))

            self.currentState=self.State.AddToLocal

        elif self.currentState == self.State.AddToLocal:
            file_syncer.copyToLocal(self.listbox.get(0, self.listbox.size()),
                                    gconfig.values['settings']['remote'],
                                    gconfig.values['settings']['local'])

            localFiles.update(set(self.listbox.get(0, self.listbox.size())))
            remoteFiles.update(set(self.listbox.get(0, self.listbox.size())))

            self.currentState=self.State.RemoveFromLocal

        elif self.currentState == self.State.RemoveFromLocal:
            file_syncer.deleteFromLocal(self.listbox.get(0, self.listbox.size()),
                                        gconfig.values['settings']['remote'],
                                        gconfig.values['settings']['local'])

            localFiles.difference_update(
                set(self.listbox.get(0, self.listbox.size())))
            remoteFiles.difference_update(
                set(self.listbox.get(0, self.listbox.size())))

            # Remember to write config to disk before exiting
            helper.writeConfigFilesToDisk(localFiles, remoteFiles, gconfig)

            exit()

        helper.writeConfigFilesToDisk(localFiles, remoteFiles, gconfig)
        self.showGUI()

    def onUpdateSelectedButtonClick(self):
        if self.currentState == self.State.AddToRemote:
            file_syncer.copyToRemote(self.listboxcurselection())
            self.currentState=self.State.RemoveFromRemote

        elif self.currentState == self.State.RemoveFromRemote:
            file_syncer.copyToRemote(self.listboxcurselection())
            self.currentState=self.State.AddToLocal

        elif self.currentState == self.State.AddToLocal:
            file_syncer.copyToRemote(self.listboxcurselection())
            self.currentState=self.State.RemoveFromLocal

        elif self.currentState == self.State.RemoveFromLocal:
            file_syncer.copyToRemote(self.listboxcurselection())
            exit()

        self.showGUI()

    def onSkipButtonClick(self):
        if self.currentState == self.State.AddToRemote:
            self.currentState=self.State.RemoveFromRemote
        elif self.currentState == self.State.RemoveFromRemote:
            self.currentState=self.State.AddToLocal
        elif self.currentState == self.State.AddToLocal:
            self.currentState=self.State.RemoveFromLocal
        elif self.currentState == self.State.RemoveFromLocal:
            exit()

        self.showGUI()


class SettingsPage(tk.Frame):

    def __init__(self, parent, controller):
        self.localDirectory=tk.StringVar()
        self.remoteDirectory=tk.StringVar()
        tk.Frame.__init__(self, parent)
        self.initializeWidgets(controller)

    def initializeWidgets(self, controller):
        # Create the grid layout manager
        self.grid()

        # Create the Local and Remote labels
        self.localLabel=tk.Label(
            self, text="Local:")
        self.remoteLabel=tk.Label(
            self, text="Remote:")

        self.localDirectoryBox=tk.Entry(
            self, width=29, textvariable=self.localDirectory)
        self.remoteDirectoryBox=tk.Entry(
            self, width=29, textvariable=self.remoteDirectory)

        # Create the cancel and save buttons
        self.cancelButton=tk.Button(
            self,
            text="Cancel",
            width=15,
            command=lambda: self.onCancelButtonClick(controller))
        self.saveButton=tk.Button(
            self,
            text="Save",
            width=15,
            command=lambda: self.onSaveButtonClick(controller))

        # Create the infobox
        self.infoBox=tk.Label(
            self, width=36, height=2, anchor='s', fg='black', bg='white', relief='ridge')

    def showGUI(self):
        self.localDirectory.set(gconfig.values['settings']['local'])
        self.remoteDirectory.set(gconfig.values['settings']['remote'])

        self.localLabel.grid(row=0, column=0, sticky='W')
        self.remoteLabel.grid(row=1, column=0, sticky='W')
        self.localDirectoryBox.grid(row=0, column=1, sticky='EW')
        self.remoteDirectoryBox.grid(row=1, column=1, sticky='EW')
        self.cancelButton.place(rely=1.0, relx=0.0, x=0, y=-26, anchor='sw')
        self.saveButton.place(rely=1.0, relx=1.0, x=0, y=-26, anchor='se')
        self.infoBox.place(rely=1.0, relx=0.5, x=0, y=-10, anchor='center')

    def onCancelButtonClick(self, controller):
        controller.showFrame(MainPage)

    def onSaveButtonClick(self, controller):
        self.localDirectory.get()
        self.remoteDirectory.get()
        gconfig.values['settings']['local']=self.localDirectory.get()
        gconfig.values['settings']['remote']=self.remoteDirectory.get()
        # All the filenames are lost here, which makes sense because
        # we changed to a new directory
        # TODO: Dont't do this if the directory is unchanged"
        gconfig.writeConfig()
        controller.showFrame(MainPage)
