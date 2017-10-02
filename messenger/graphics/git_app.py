from subprocess import getoutput
from PyQt5 import QtWidgets

from utils.logger import Logger


class GitApplication(QtWidgets.QWidget, Logger):

    def __init__(self):
        super().__init__()

    def check_update(self):

        self.log("I check for updates.")
        getoutput("git fetch")
        git_msg = getoutput("git diff origin/master")
        self.log("Git message is: '{}'".format(git_msg))

        if git_msg:

            if self.show_question(
                    "An update is available.",
                    question="Do you want to update now?", yes="Yes", no="No", focus="Yes"):

                git_output = getoutput("git pull")
                self.log("User wants to update. Git message is: {}".format(git_output))
                success = 0

                if "Updating" in git_output:
                    success = 1

                else:
                    for msg in ["git stash", "git pull", "git stash pop"]:
                        git_output = getoutput(msg)
                        self.log("Command is '{}' Git message is: '{}'".format(msg, git_output))

                    if "Updating" in git_output:
                        success = 1

                if success:
                    self.show_info("Updated successfully. Modifications will be effective at the next restart.")

                else:
                    self.show_warning("An error occurred. No modifications have been done.")