from Views.testExplorer import TestExplorer  # the test explorer
from Model.test import Test  # the test class (used to initialize the test explorer)
from PyQt5.QtWidgets import *  # this module contains classes that provide a set of UI elements to create classic desktop-style user interfaces
import sys
import os
import getopt

def main():
    tests = getTestsRelativeToCurrentDirectory("..,Impact") #  generate tests based on impact folder

    try:
        opts, args = getopt.getopt(sys.argv[1:], "a", ["runall"])
    except getopt.GetoptError:
        print('Could not create command line arguments')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-a", "--runall"):
            [test.run() for test in tests]
            [test.assertMatchingCounts() for test in tests]
            return

    app = QApplication(sys.argv) #  create instance of Q application. Should only have one even if you have multiple windows
    testExplorer = TestExplorer(tests) #  generate the test explorer with the tests
    testExplorer.show() #  show the test explorer
    app.exec_() #  execute the application

def getTestsRelativeToCurrentDirectory(relativePathString):
    currentDir = os.getcwd()
    testsPath = os.path.abspath(os.path.join(currentDir, *relativePathString.split(',')))

    subFolders = os.listdir(testsPath)

    # remove ImpactCommon if it exists. This folder contains the common impact messages
    if ("ImpactCommon" in subFolders):
        subFolders.remove("ImpactCommon")

    testDirs = [os.path.abspath(os.path.join(testsPath, folder)) for folder in subFolders]
    # generate all the tests
    tests = [Test(testDir) for testDir in testDirs]

    return tests

if __name__ == '__main__':
    main()
