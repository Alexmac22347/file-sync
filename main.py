#!/usr/bin/python
# Code from:
# http://sebsauvage.net/python/gui/#our_project

import Tkinter as tk

WINHEIGHT = 450
WINWIDTH = 296

class simpleapp_tk(tk.Tk):

    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        # Create the grid layout manager
        self.grid()
        # This thing is not going to be resizable
        self.resizable(width=False, height=False)
        self.geometry('{}x{}'.format(WINWIDTH,WINHEIGHT))

        # Create listbox with vertical and horizontal scroll
        # Create the vertical scroll
        self.yScroll = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.yScroll.grid(row=0, column=1, sticky=tk.N+tk.S)
        # Create the horizontal scroll
        self.xScroll = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.xScroll.grid(row=1, column=0, sticky=tk.E+tk.W)
        # Create the listbox
        self.listbox = tk.Listbox(self, activestyle='none',
                height=20,
                width=35,
                xscrollcommand=self.xScroll.set,
                yscrollcommand=self.yScroll.set)
        self.listbox.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.xScroll['command'] = self.listbox.xview
        self.yScroll['command'] = self.listbox.yview

        for i in range(20):
            self.listbox.insert(i,"Hello {}".format(i))

    def OnButtonClick(self):
        print "You clicked the button !"

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('File Sync')
    app.mainloop()
