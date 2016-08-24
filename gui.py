import Tkinter as tk
import config

WINHEIGHT = 445
WINWIDTH = 296

config = config.config()


class gui(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.grid()
        # This thing is not going to be resizable
        self.resizable(width=False, height=False)
        self.geometry('{}x{}'.format(WINWIDTH, WINHEIGHT))

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
            config.values['paths'] = {}
            config.values['paths']['local'] = '/home/alex/Music/'
            config.values['paths']['remote'] = 'SD\ Card/Music/'
            config.writeConfig()
            config.readConfig()


    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


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
        self.showGUI()

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
            command=lambda: controller.showFrame(SettingsPage))

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
        # if we're not in settings
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
    def onSettingsButtonClick(self):
        gui.showFrame(SettingsPage)

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
        self.showGUI()

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
        config.readConfig()
        self.localDirectory.set(config.values['paths']['local'])
        self.remoteDirectory.set(config.values['paths']['remote'])

        self.localLabel.grid(row=0, column=0, sticky='W')
        self.remoteLabel.grid(row=1, column=0, sticky='W')
        self.localDirectoryBox.grid(row=0, column=1, sticky='EW')
        self.remoteDirectoryBox.grid(row=1, column=1, sticky='EW')
        self.cancelButton.place(rely=1.0, relx=0.0, x=0, y=-26, anchor='sw')
        self.saveButton.place(rely=1.0, relx=1.0, x=0, y=-26, anchor='se')
        self.infoBox.place(rely=1.0, relx=0.5, x=0, y=-10, anchor='center')

    def onCancelButtonClick(self, controller):
        controller.showFrame(MainPage)
