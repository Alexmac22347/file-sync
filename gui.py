""" A GUI which the user can interact with. Contains multiple frames"""

import Tkinter as tk
import selection_state
import file_syncer

WINHEIGHT = 445
WINWIDTH = 296

# This object is accessible from all classes
fileSyncer = file_syncer.globalFileSyncer


class gui(tk.Tk):
    """The Gui class which displays frames in a window"""

    def __init__(self, *args, **kwargs):
        """Create the main window. The MainPage frame is then shown"""

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

    def showFrame(self, cont):
        """Displays the frame "cont"

        Args:
            cont: The frame to be displayed

        Returns:
            Nothing

        """

        frame = self.frames[cont]
        frame.tkraise()
        frame.showGUI()


class MainPage(tk.Frame):
    """This frame displays multiple files which the user can select.

    Depending on the current state, locally added, locally removed,
    remotely added, or remotely removed files will be displayed.
    The user can the select what to do with these files (either
    update or ignore). A settings button is also present

    """

    def __init__(self, parent, controller):
        """Initialize the page and show the appropriate widgets

        The initial state is AddToRemote, which displays
        locally added files which the user may want to
        add to the remote directory.

        """

        self.currentState = selection_state.AddToRemote
        tk.Frame.__init__(self, parent)
        self.initializeWidgets(controller)

    def initializeWidgets(self, controller):
        """Create the widget objects"""

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
            command=lambda: self.onUpdateButtonClick(True),
            width=28)

        # Create the "update selected" button
        self.updateSelectedButton = tk.Button(
            self, text="Add selected to remote",
            command=lambda: self.onUpdateButtonClick(False))

        # Create the "skip" button
        self.skipButton = tk.Button(
            self, text="Skip", command=self.onSkipButtonClick)

        # Create the info box
        self.infoBox = tk.Label(
            self, width=30, height=2, anchor='nw', fg='black', bg='white', relief='ridge', justify=tk.LEFT)

    def showGUI(self):
        """Displays the widgets on the screen"""

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

        if self.currentState == selection_state.AddToRemote:
            for filename in sorted(list(fileSyncer.addedToLocal), reverse=True):
                self.listbox.insert(0, filename)

            if fileSyncer.addedToLocal:
                self.infoBox['text'] = "These files have been added to " + \
                    fileSyncer.gconfig.values['settings']['local']
            else:
                self.infoBox['text'] = "No new files in " + \
                    fileSyncer.gconfig.values['settings']['local']

            self.updateAllButton['text'] = "Copy all to remote"
            self.updateSelectedButton['text'] = "Copy selected to remote"

        elif self.currentState == selection_state.RemoveFromRemote:
            for filename in sorted(list(fileSyncer.removedFromLocal), reverse=True):
                self.listbox.insert(0, filename)

            if fileSyncer.removedFromLocal:
                self.infoBox['text'] = "These files have been deleted from " + \
                    fileSyncer.gconfig.values['settings']['local']
            else:
                self.infoBox['text'] = "No deleted files in " + \
                    fileSyncer.gconfig.values['settings']['local']

            self.updateAllButton['text'] = "Remove all from remote"
            self.updateSelectedButton['text'] = "Remove selected from remote"

        elif self.currentState == selection_state.AddToLocal:
            for filename in sorted(list(fileSyncer.addedToRemote), reverse=True):
                self.listbox.insert(0, filename)

            if fileSyncer.addedToRemote:
                self.infoBox['text'] = "These files have been added to (Device)" + \
                    fileSyncer.gconfig.values['settings']['remote']
            else:
                self.infoBox['text'] = "No new files in (Device)" + fileSyncer.gconfig.values['settings']['remote']

            self.updateAllButton['text'] = "Copy all to local"
            self.updateSelectedButton['text'] = "Copy selected to local"

        elif self.currentState == selection_state.RemoveFromLocal:
            for filename in sorted(list(fileSyncer.removedFromRemote), reverse=True):
                self.listbox.insert(0, filename)

            if fileSyncer.removedFromRemote:
                self.infoBox['text'] = "These files have been deleted from (Device)" + \
                    fileSyncer.gconfig.values['settings']['remote']
            else:
                self.infoBox[
                    'text'] = "No deleted files in (Device)" + fileSyncer.gconfig.values['settings']['remote']

            self.skipButton['text'] = "Quit"
            self.updateAllButton['text'] = "Remove all from local"
            self.updateSelectedButton['text'] = "Remove selected from local"

    # Various event handlers
    def onSettingsButtonClick(self, controller):
        """Show the settings page if settings button is pressed"""

        controller.showFrame(SettingsPage)

    def onUpdateButtonClick(self, selectAll):
        """Update selected files when the update button is pressed""" 

        selectedFiles = []

        if selectAll:
            selectedFiles = self.listbox.get(0, self.listbox.size())
        else:
            for index in self.listbox.curselection():
                selectedFiles.append(self.listbox.get(index))

        fileSyncer.onUpdateButtonClick(self.currentState, selectedFiles)

        self._advanceState()
        self.showGUI()

    def onSkipButtonClick(self):
        """Skip to the next state if the skip button is pressed"""

        self._advanceState()
        self.showGUI()

    def _advanceState(self):
        """Helper function to move to the next state"""

        if self.currentState == selection_state.AddToRemote:
            self.currentState = selection_state.RemoveFromRemote
        elif self.currentState == selection_state.RemoveFromRemote:
            self.currentState = selection_state.AddToLocal
        elif self.currentState == selection_state.AddToLocal:
            self.currentState = selection_state.RemoveFromLocal
        elif self.currentState == selection_state.RemoveFromLocal:
            exit()


class SettingsPage(tk.Frame):

    def __init__(self, parent, controller):
        """Initialize the widgets and the string variables

        The string variables are the strings contained in the
        settings page boxed. These can be manipulated by the user

        """

        self.localDirectoryText = tk.StringVar()
        self.remoteDirectoryText = tk.StringVar()
        tk.Frame.__init__(self, parent)
        self.initializeWidgets(controller)

    def initializeWidgets(self, controller):
        """Create the widget objects"""

        # Create the grid layout manager
        self.grid()

        # Create the Local and Remote labels
        self.localLabel = tk.Label(
            self, text="Local:")
        self.remoteLabel = tk.Label(
            self, text="Remote:")

        self.localDirectoryBox = tk.Entry(
            self, width=29, textvariable=self.localDirectoryText)
        self.remoteDirectoryBox = tk.Entry(
            self, width=29, textvariable=self.remoteDirectoryText)

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
        """Display the widget objects on the screen"""

        self.localDirectoryText.set(fileSyncer.gconfig.values['settings']['local'])
        self.remoteDirectoryText.set(fileSyncer.gconfig.values['settings']['remote'])

        self.localLabel.grid(row=0, column=0, sticky='W')
        self.remoteLabel.grid(row=1, column=0, sticky='W')
        self.localDirectoryBox.grid(row=0, column=1, sticky='EW')
        self.remoteDirectoryBox.grid(row=1, column=1, sticky='EW')
        self.cancelButton.place(rely=1.0, relx=0.0, x=0, y=-26, anchor='sw')
        self.saveButton.place(rely=1.0, relx=1.0, x=0, y=-26, anchor='se')
        self.infoBox.place(rely=1.0, relx=0.5, x=0, y=-10, anchor='center')

    def onCancelButtonClick(self, controller):
        """Go back to the MainPage if cancel button is pressed"""

        controller.showFrame(MainPage)

    def onSaveButtonClick(self, controller):
        """Save the users entry to the config file, the return
        to the MainPage"""

        # TODO: Do this in the file syncer?
        # TODO: Review this logic. Why do I get it twice?
        self.localDirectoryText.get()
        self.remoteDirectoryText.get()

        fileSyncer.gconfig.values['settings']['local'] = self.localDirectoryText.get()
        fileSyncer.gconfig.values['settings']['remote'] = self.remoteDirectoryText.get()

        fileSyncer.gconfig.writeConfig()
        controller.showFrame(MainPage)
