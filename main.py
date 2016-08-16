#!/usr/bin/python
# Code from:
# http://sebsauvage.net/python/gui/#our_project

import Tkinter


class simpleapp_tk(Tkinter.Tk):

    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        # Create the grid layout manager
        self.grid()

        # Add the text entry box
        # Remember what was entered into the box
        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self, textvariable=self.entryVariable)
        self.entry.grid(column=0, row=0, sticky='EW')
        # Add handler for when user presses enter
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Enter text here")

        # Add the button
        # Also add handler when this button is clicked
        button = Tkinter.Button(self, text=u"Click Me",
                                command=self.OnButtonClick)
        button.grid(column=1, row=0)

        # Create the blue label thing
        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self, textvariable=self.labelVariable,
                              anchor="w", fg="white", bg="blue")
        label.grid(column=0, row=1, columnspan=2, sticky='EW')

        # Tell the layout manager to resize its columns and rows when
        # the window is resized
        self.grid_columnconfigure(0, weight=1)
        # Only allow vertical resizing
        self.resizable(True, False)
        # Dont resize the window if long text is entered
        self.update()
        self.geometry(self.geometry())


    def OnButtonClick(self):
        self.labelVariable.set(self.entryVariable.get()) 
                               
        print "You clicked the button !"

    def OnPressEnter(self, event):
        self.labelVariable.set(self.entryVariable.get())
        print "You Pressed enter !"


if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('File Sync')
    app.mainloop()
