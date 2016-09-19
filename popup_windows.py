import Tkinter as tk


def promptUserForDirectories():
    """Prompts user for local and remote directories.
    Returns a tuple containing two strings. The first is 
    the local directory and second is the remote directory"""

    popup = tk.Tk()
    popup.resizable(width=False, height=False)
    popup.geometry('270x100')
    popup.grid()

    label = tk.Label(popup, text="Enter Remote and Local Directories:")
    label.grid(row=0,column=0,columnspan=2,sticky='W')

    localDirectoryText = tk.StringVar()
    remoteDirectoryText = tk.StringVar()

    # Create the Local and Remote labels
    localLabel = tk.Label(
        text="Local:")
    remoteLabel = tk.Label(
        text="Remote:")

    localDirectoryBox = tk.Entry(width=25,
        textvariable=localDirectoryText)
    remoteDirectoryBox = tk.Entry(width=25,
        textvariable=remoteDirectoryText)

    localLabel.grid(row=1, column=0, sticky='W')
    remoteLabel.grid(row=2, column=0, sticky='W')
    localDirectoryBox.grid(row=1, column=1, sticky='EW')
    remoteDirectoryBox.grid(row=2, column=1, sticky='EW')

    # Create the cancel and save buttons
    exitButton = tk.Button(popup, width=10, text="Exit", command = exit)
    exitButton.place(x=20,y=65)
    saveButton = tk.Button(popup, width=10, text="Save", command = popup.destroy)
    saveButton.place(x=150,y=65)

    popup.mainloop()
    return (localDirectoryText.get(), remoteDirectoryText.get())

def errorMessagePopup(message):
    """Display message. Also has a button to close the popup window"""

    popup = tk.Tk()

    label = tk.Label(text=message)
    label.pack()

    exitButton = tk.Button(popup, text="Okay", command=popup.destroy)
    exitButton.pack()

    popup.mainloop()
