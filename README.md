Use this to sync files between a phone and PC.
You don't have to remember which files you removed/added 
to your phone/pc
Eg, if you put a huge compilation on your phone,
    then go through and delete songs you dont like
    from your phone, you can delete the same songs
    from your pc as well.

Note: tested only on linux mint and Samsung Galaxy S4.
Your phone must use MTP.

How to use:  
1.) When using for the first time, make sure your phone folder
and PC folder are synced (the folders you are syncing have the 
exact same files and folders)  
2.) Plug in a SINGLE phone  
3.) Run the program  
4.) A config.ini file containing a list of all the files in the local and remote directories will be created.

Now, anytime you add or remove a file in the remote or local directory, 
this will be detected, and you will be asked if you want to "mirror"
the change in the other directory.

Note: If you delete the SAME file from the local AND remote directory,
or add the SAME file to the local AND remote directory, the change will
be reflected in the config.ini file, but will not appear in the user interface.


TODO:
- Display error if single phone not detected
- Add support for USB mass storage
- Allow window resizing
- Detect file changes with md5?
- Get rid of helper module
