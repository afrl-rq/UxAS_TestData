import getpass
import os
import platform
import subprocess

from Model.Enums.testStatus import TestStatus
from Services.fileHelper  import FileHelper
from Services.uxasDbHelper import UxASDbHelper


#A class containing the logic for test information, setup, verification, and execution of a test

class Test():
    def __init__(self, folderPath):
        self.folderPath = folderPath # the test's folder path
        self.description = "This test is still pending."
        self.status = TestStatus.Pending # the current status of the test
        self.name = os.path.basename(os.path.normpath(self.folderPath)) # the name of the test
        self.acceptedDbPath =  self.getAcceptedDbPath() # the fully quialified path of the accepted database
        self.testScript = self.getTestScript() # the fully qualified path of the test
        self.testDbPath = "" # the fully qualified path of the test database

    #NOTE: FOR THE EXECUTION OF A TEST ON WINDOWS, THE USER MUST KNOW THE PATH OF GIT-BASH
    #the run method runs the test and updates the generatedDbLocation
    # TODO: FINISH THIS METHOD. IS NOT TOTALLY FUNCTIONAL YET (windows test only works on my machine)
    def run(self):
        #first update the status of the test
        self.status = TestStatus.Executing
        self.description = "This test is currently executing."

        if (self.isValidTest()):
            process = subprocess
            if (platform.system() == 'Windows'):  # if on windows use git-bash to execute the shell script
                # TODO: CHANGE gitPath VARIABLE TO A RELATIVE PATH
                # if on windows I hope this is always saved in the same location
                user = getpass.getuser()
                gitPath = r'C:\Users\\' + user + '\AppData\Local\Programs\Git\git-bash.exe'
                # need to change directory or will not save the new db in appropriate location
                dir = os.path.split(os.path.abspath(self.testScript))[0]
                os.chdir(dir)
                #start the subprocess
                #process = subprocess.run("%s %s" % (gitPath, self.testScript))
                process = subprocess.Popen("%s %s" % (gitPath, self.testScript))

            else:  # otherwise can just call the script as a subpath
                # TODO: TEST THIS CALL ON LINUX/MACOS
                process = subprocess.call(self.testScript)
            # TODO: ADD A TIMEOUT FOR DURATION OF UxAS TO EXECUTE. CURRENTLY USER NEEDS TO PRESS CTRL+C TO EXIT OR ADDED TO UxAS SCRIPT
            process.wait()


    #should update the status and description of the test
    def assertMatchingCounts(self):
        self.updateGeneratedDbPath()
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
        if (self.acceptedDbPath != None and self.testScript != None):
            return True
        return False

    def updateGeneratedDbPath(self):
        #get the location of the generatedDb
        testDirData = FileHelper.searchForSubFolderInDir(self.folderPath, "RUNDIR", True)
        if(testDirData[0]):
            testDir = testDirData[1] + r"\datawork\SavedMessages"

        testPath = FileHelper.getMostRecentFileInPathWithExtension(testDir, ".db3")

        #set the generatedDbLocation
        if(testPath[0]):
            self.testDbPath = testPath[1]
        else:
            self.testDbPath = None

    def getTestScript(self):
        testScriptData = FileHelper.searchForFileInDir(self.folderPath, "runUxAS", True )
        if(testScriptData[0]):
            return testScriptData[1]
        return None

    def getAcceptedDbPath(self):
        subFolder = FileHelper.searchForSubFolderInDir(self.folderPath, "Accepted", True)
        if(subFolder[0]):
            mostRecentFile = FileHelper.getMostRecentFileInPathWithExtension(subFolder[1], ".db3")
            if(mostRecentFile[0]):
                return mostRecentFile[1]
        return None

    def toHtml(self):
        htmlDescription = self.description.replace("\n","<br/>")
        #not sure if the pages breaks are necessary yet...
        return "<h1><b>{}</b></h1>" \
               "<h3>Status: {}</h3>" \
               "<pre>Description: <br/>{}</pre>".format(self.name, self.status.name, self.description)

    def print(self):
        print("\n\n\nTest: " + self.name + " " + (self.status.name) + "\n\t" + self.description)