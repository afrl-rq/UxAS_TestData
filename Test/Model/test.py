import getpass
import os
import platform
import subprocess

from Model.Enums.testStatus import TestStatus
from Services.fileHelper  import FileHelper
from Services.uxasDbHelper import UxASDbHelper


#A class containing the logic for test information, setup, verification, and execution of a test
class Test():
    """The model for the tests.
    Contains the logic for test setup, verification, and execution
    """
    def __init__(self, folderPath):
        self.folderPath = folderPath # the test's folder path
        self.description = "This test is still pending."
        self.status = TestStatus.Pending # the current status of the test
        self.name = os.path.basename(os.path.normpath(self.folderPath)) # the name of the test
        self.acceptedDbPath =  self.getAcceptedDbPath() # the fully qualified path of the accepted database
        self.testScript = self.getTestScript() # the fully qualified path of the test
        self.testDbPath = None # the fully qualified path of the test database

    #the run method runs the test and updates the generatedDbLocation
    def run(self):
        """Executes the test.
         The resultant database should be checked against the accepted database.
        :return: Void
        """
        #first update the status of the test
        self.status = TestStatus.Executing
        self.description = "This test is executing."

        if (self.isValidTest()):
            process = subprocess
            if (platform.system() == 'Windows'):  # if on windows use git-bash to execute the shell script
                # hopefully git is always saved in the same location on windows systems
                user = getpass.getuser()
                gitPath = r'C:\Users\\' + user + '\AppData\Local\Programs\Git\git-bash.exe'
                # need to change directory or will not save the new db in appropriate location
                dir = os.path.split(os.path.abspath(self.testScript))[0]
                os.chdir(dir)
                #start the subprocess
                #process = subprocess.run("%s %s" % (gitPath, self.testScript))
                process = subprocess.Popen("%s %s" % (gitPath, self.testScript))

            else:  # otherwise can just call the script as a subpath
                dir = os.path.split(os.path.abspath(self.testScript))[0]
                os.chdir(dir)
                process = subprocess.Popen([self.testScript])
            process.wait()

    def assertMatchingCounts(self):
        """Checks if the message counts in the accepted and test databases match.
         Updates the status of the test
        :return: Void
        """
        if not (self.isValidTest()):
            return

        self.updateGeneratedDbPath()
        if (self.testDbPath == None):
            return
        truthDescriptorAndCounts = UxASDbHelper.getDescriptorAndCounts(self.acceptedDbPath)
        testDescriptorAndCounts = UxASDbHelper.getDescriptorAndCounts(self.testDbPath)
        testData = UxASDbHelper.compareDescriptorAndCounts(truthDescriptorAndCounts, testDescriptorAndCounts, self.name)

        # update the test status
        if (testData[0]):
            self.status = TestStatus.Passed
        else:
            self.status = TestStatus.Failed
        #update the description
        self.description = testData[1]

    def isValidTest(self): # this should be checked before running a test. Could show test in testExplorer even if is not valid. Should have warning test status selector
        #for the test to be valid, there must be two files located in the folder...:
            #  there is an acceptedDb
            #  there is a runUxAS script
        """Checks if the test is valid (contains an actual database and has a script to run the test)
        :return: Boolean - true if both the accepted database and test script are set, false either is not set.
        """
        if (self.acceptedDbPath != None and self.testScript != None):
            return True
        return False

    def updateGeneratedDbPath(self):
        """Updates the path to the generated database (testScriptData property) after the test has run
        :return: Void
        """
        #get the location of the generatedDb
        testDirData = FileHelper.searchForSubFolderInDir(self.folderPath, "RUNDIR", True)

        testDir = ""

        if(testDirData[0]):
            testDir = os.path.join(testDirData[1], *",datawork,SavedMessages,".split(','))
            testPath = FileHelper.getMostRecentFileInPathWithExtension(testDir, ".db3")
            #set the generatedDbLocation
            if(testPath[0]):
                self.testDbPath = testPath[1]


    def getTestScript(self):
        """Searches for the test script and returns its value
        :return: String - test script path
        """
        testScriptData = FileHelper.searchForFileInDir(self.folderPath, "runUxAS", True )
        if(testScriptData[0]):
            return testScriptData[1]
        return None

    def getAcceptedDbPath(self):
        """Returns the accepted database if it exists. This is found in the Accepted folder within each test folder.
        :return: String - database path
        """
        subFolder = FileHelper.searchForSubFolderInDir(self.folderPath, "Accepted", True)
        if(subFolder[0]):
            mostRecentFile = FileHelper.getMostRecentFileInPathWithExtension(subFolder[1], ".db3")
            if(mostRecentFile[0]):
                return mostRecentFile[1]
        return None

    def toHtml(self):
        """ Returns a HTML representation of the test based on the name of the test, status of the test, and description of the test.
        :return: String - HTML format
        """
        htmlDescription = self.description.replace("\n","<br/>")

        return "<h1><b>{}</b></h1>" \
               "<h3>Status: {}</h3>" \
               "<pre>Description: <br/>{}</pre>".format(self.name, self.status.name, self.description)

    def print(self):
        """ Prints the name, status, and descirption of the test to the console
        :return: Void
        """
        print("\n\n\nTest: " + self.name + " " + (self.status.name) + "\n\t" + self.description)