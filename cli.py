import file_syncer
import os
import selection_state
import distutils.sysconfig
from distutils.util import strtobool

# This object is accessible from all classes
fileSyncer = file_syncer.globalFileSyncer

class Cli:
    def run(self):
        # Get the files added locally.
        # Ask if they should be copied over to remote
        files_added_to_local = sorted(list(fileSyncer.addedToLocal), reverse=True)
        self.prompt_user(
                files_added_to_local, 
                "These files were added to local.\nCopy to remote? (y/n)",
                copy_to_remote)

        # Get the files added to remote.
        # Ask if they should be copied over to local
        files_added_to_remote = sorted(list(fileSyncer.addedToRemote), reverse=True)
        self.prompt_user(
                files_added_to_remote, 
                "These files were added to remote.\nCopy to local? (y/n)",
                copy_to_local)


        # Get the files removed locally.
        # Ask if they should be removed from remote
        files_removed_from_local = sorted(list(fileSyncer.removedFromLocal), reverse=True)
        self.prompt_user(
                files_removed_from_local,
                "These files were removed from local.\nRemove from remote? (y/n)",
                remove_from_remote)

        # Get the files removed from remote.
        # Ask if they should be removed from local
        files_removed_from_remote = sorted(list(fileSyncer.removedFromRemote), reverse=True)
        self.prompt_user(
                files_removed_from_remote, 
                "These files were removed from remote.\nRemove from local? (y/n)",
                remove_from_local)

    def prompt_user(self, file_list, prompt, action):
        os.system('clear')

        if len(file_list) > 0:
            print_blue(prompt)
            display_files(file_list)
            while True:
                try:
                    do_action = strtobool(raw_input())
                    if do_action:
                        action(file_list)
                    break
                except ValueError:
                    print "Enter y/n"
            os.system('clear')


def copy_to_remote(file_list):
    fileSyncer.onUpdateButtonClick(selection_state.AddToRemote, file_list)

def copy_to_local(file_list):
    fileSyncer.onUpdateButtonClick(selection_state.AddToLocal, file_list)

def remove_from_remote(file_list):
    fileSyncer.onUpdateButtonClick(selection_state.RemoveFromRemote, file_list)

def remove_from_local(file_list):
    fileSyncer.onUpdateButtonClick(selection_state.RemoveFromLocal, file_list)

def display_files(files):
    for ifile in files:
        print ifile

def print_blue(text):
    print Colors.BOLD + Colors.OKBLUE
    print text
    print Colors.ENDC
        
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
