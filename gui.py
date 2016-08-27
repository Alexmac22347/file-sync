import Tkinter as tk
import config
import file_syncer

WINHEIGHT = 445
WINWIDTH = 296

# Use a global config class
# to read from disk, and see that change in all classes/pages
config = config.globalConfig


class gui(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # This thing is not going to be resizable
        self.resizable(width=False, height=False)
        self.geometry('{}x{}'.format(WINWIDTH, WINHEIGHT))

        container = tk.Frame(self)
        container.grid()

        # This dictionary contains the two Frames,
        # MainPage and SettingsPage
        self.frames = {}
        for F in (MainPage, SettingsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.showFrame(MainPage)

        # Read the config file. If it is
        # empty, initialize it
        config.readConfig()
        if not config.values:
            # TODO: prompt user for paths
            print "Initializing configuration file"
            config.values['settings'] = {}
            config.values['settings']['local'] = '/home/alex/Music/'
            config.values['settings']['remote'] = 'Card/Music/'

            config.values['files'] = {}
            config.values['files']['local'] = ""
            config.values['files']['remote'] = ""
            for filename in file_syncer.getLocalFileNames(config.values['settings']['local']):
                config.values['files']['local'] += filename + "\n"
            for filename in file_syncer.getRemoteFileNames(config.values['settings']['remote']):
                config.values['files']['remote'] += filename + "\n"

            config.writeConfig()
            # TODO: This is probably pointless
            config.readConfig()

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
            self, height=2, anchor='s', fg='black', bg='white', relief='ridge')

    # This will draw the GUI based on the current state
    def showGUI(self):
        # These things here will always be visible
        self.listbox.grid(row=0, column=0, sticky='NSEW')
        self.settingsButton.grid(row=2, column=0, sticky='EN')
        self.updateAllButton.grid(row=2, column=0, sticky='W')
        self.updateSelectedButton.grid(
            row=3, column=0, sticky='EW')
        self.skipButton.grid(row=4, column=0, sticky='EW')
        self.infoBox.grid(row=5, column=0, sticky='EW')

        if self.currentState == self.State.AddToRemote:
            self.updateAllButton['text'] = "Add all to remote"
            self.updateSelectedButton['text'] = "Add selected to remote"
            return

        if self.currentState == self.State.RemoveFromRemote:
            self.updateAllButton['text'] = "Remove all from remote"
            self.updateSelectedButton['text'] = "Remove selected from remote"
            return

        if self.currentState == self.State.AddToLocal:
            self.updateAllButton['text'] = "Add all to local"
            self.updateSelectedButton['text'] = "Add selected to local"
            return

        if self.currentState == self.State.RemoveFromLocal:
            self.updateAllButton['text'] = "Remove all from local"
            self.updateSelectedButton['text'] = "Remove selected from local"
            return

    # Various event handlers
    def onSettingsButtonClick(self, controller):
        controller.showFrame(SettingsPage)

    def onUpdateAllButtonClick(self):
        if self.currentState == self.State.AddToRemote:
            self.currentState = self.State.RemoveFromRemote
        elif self.currentState == self.State.RemoveFromRemote:
            self.currentState = self.State.AddToLocal
        elif self.currentState == self.State.AddToLocal:
            self.currentState = self.State.RemoveFromLocal
        elif self.currentState == self.State.RemoveFromLocal:
            exit()

        self.showGUI()

    def onUpdateSelectedButtonClick(self):
        if self.currentState == self.State.AddToRemote:
            self.currentState = self.State.RemoveFromRemote
        elif self.currentState == self.State.RemoveFromRemote:
            self.currentState = self.State.AddToLocal
        elif self.currentState == self.State.AddToLocal:
            self.currentState = self.State.RemoveFromLocal
        elif self.currentState == self.State.RemoveFromLocal:
            exit()

        self.showGUI()

    def onSkipButtonClick(self):
        if self.currentState == self.State.AddToRemote:
            self.currentState = self.State.RemoveFromRemote
        elif self.currentState == self.State.RemoveFromRemote:
            self.currentState = self.State.AddToLocal
        elif self.currentState == self.State.AddToLocal:
            self.currentState = self.State.RemoveFromLocal
        elif self.currentState == self.State.RemoveFromLocal:
            exit()

        self.showGUI()


class SettingsPage(tk.Frame):

    def __init__(self, parent, controller):
        self.localDirectory = tk.StringVar()
        self.remoteDirectory = tk.StringVar()
        tk.Frame.__init__(self, parent)
        self.initializeWidgets(controller)

    def initializeWidgets(self, controller):
        # Create the grid layout manager
        self.grid()

        # Create the Local and Remote labels
        self.localLabel = tk.Label(
            self, text="Local:")
        self.remoteLabel = tk.Label(
            self, text="Remote:")

        # Create the local and remote directory text entry boxes
        self.localDirectoryBox = tk.Entry(
            self, width=29, textvariable=self.localDirectory)
        self.remoteDirectoryBox = tk.Entry(
            self, width=29, textvariable=self.remoteDirectory)

        # Create the cancel and save buttons
        self.cancelButton = tk.Button(
            self,
            text="Cancel",
            width=15,
            command=lambda: self.onCancelButtonClick(controller))
        self.saveButton = tk.Button(
            self,
            text="Save",
            width=15,
            command=lambda: self.onSaveButtonClick(controller))

        # Create the infobox
        self.infoBox = tk.Label(
            self, width=36, height=2, anchor='s', fg='black', bg='white', relief='ridge')

    def showGUI(self):
        self.localDirectory.set(config.values['settings']['local'])
        self.remoteDirectory.set(config.values['settings']['remote'])

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
        config.values['settings']['local'] = self.localDirectory.get()
        config.values['settings']['remote'] = self.remoteDirectory.get()
        config.writeConfig()
        controller.showFrame(MainPage)
