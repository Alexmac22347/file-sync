#!/usr/bin/python

import Tkinter as tk

WINHEIGHT = 450
WINWIDTH = 296


class gui(tk.Tk):

    # This is used to represent what part of the program we are in.
    # It will help determine what to do when a button is pressed,
    # and what files to display in the list box
    class State:
        AddToRemote = 1
        RemoveFromRemote = 2
        AddToLocal = 3
        RemoveFromLocal = 4


    def __init__(self, parent):
        # The program starts is the "Add to remote" state
        self.currentState = self.State.AddToRemote

        #TODO: Load the right local and remote directories
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.initializeWidgets()
        self.showGUI()

    def initializeWidgets(self):
        # Create the grid layout manager
        self.grid()
        # This thing is not going to be resizable
        self.resizable(width=False, height=False)
        self.geometry('{}x{}'.format(WINWIDTH, WINHEIGHT))

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
            self, image=self.settingsIcon, command=self.onSettingsButtonClick)

        # Create the "update all" button
        self.updateAllButton = tk.Button(
            self, text="Add all to remote", command=self.onUpdateAllButtonClick)

        # Create the "update selected" button
        self.updateSelectedButton = tk.Button(
            self, text="Add selected to remote",
            command=self.onUpdateSelectedButton)

    # This will draw the GUI based on the current state
    def showGUI(self):
        # These things here will always be visible
        # if we're not in settings
        self.listbox.grid(row=0, column=0, sticky='NSEW')
        self.settingsButton.grid(row=2, column=0, sticky='EN')
        self.updateAllButton.grid(row=2, column=0, sticky='WN')
        self.updateSelectedButton.grid(
            row=3, column=0, sticky='WN')

        if self.currentState == self.State.AddToRemote:
            return

        if self.currentState == self.State.RemoveFromRemote:
            pass

        if self.currentState == self.State.AddToLocal:
            pass

        if self.currentState == self.State.RemoveFromLocal:
            pass

    # Various event handlers
    def onSettingsButtonClick(self):
        print "You clicked the settings icon"

    def onUpdateAllButtonClick(self):
        print "You selected all"

    def onUpdateSelectedButton(self):
        print "You selected specific files"
