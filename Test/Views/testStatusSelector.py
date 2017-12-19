#this is the test status selector.
# 1. set label to Test Status
# 2. create a QListView with the tests passed during initialization
# 3. create a QWebEngineView using the .toHtml method in the test class

import os

from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *

from Model.Enums.testStatus import TestStatus


class StatusView(QDialog):
    def __init__(self, tests):
        QDialog.__init__(self)  # call constructor of parent class
        self.tests = tests # hang on to those tests. They're needed to run the selected tests
        self.testIterator = 0
        # set the layout
        layout = QHBoxLayout()  # put everything in the layout in a grid
        self.setWindowTitle("Test Status")

        ######################################################################
        #                        SETUP THE WIDGETS                          #
        ######################################################################
        # setup the list view
        self.listModel = ItemListModel(self.tests,self)
        self.listView = QListView()
        self.listView.setModel(self.listModel)

        self.listView.clicked.connect(self.selectedTestChanged)

        #setup the web engine view
        self.webView = QWebEngineView()
        self.webView.setHtml("<h1>Executing Test(s)...</h1>")
        #try resizing the webView... Not sure why this doesnt work
        self.webView.resize(100,100)


        #ADD A TIMER TO UPDATE THE LISTVIEW's ITEMS EVERY 5 SECONDS
        self.checkThreadTimer = QTimer(self)
        self.checkThreadTimer.setInterval(500) #interval to run the tests, then check if they passed
        self.checkThreadTimer.timeout.connect(self.runTests)
        self.checkThreadTimer.setSingleShot(True)


        ######################################################################
        #                         SETUP THE LAYOUT                           #
        ######################################################################
        layout.addWidget(self.listView)
        layout.addWidget(self.webView)

        self.setLayout(layout)
        self.checkThreadTimer.start()

    ######################################################################
    #                SOME HANDLERS FOR THE WIDGET EVENTS                 #
    ######################################################################

    def closeEvent(self, QCloseEvent):
        os.system('cls' if os.name =='nt' else 'clear')
        for test in self.tests:
            test.status = TestStatus.Pending

    def selectedTestChanged(self):
        selectedIndex = self.listView.selectedIndexes()[0]
        selectedTestHtml = self.listModel.listData[selectedIndex.row()].toHtml()
        self.webView.setHtml(selectedTestHtml)

    def runTests(self):
        """
        Runs the next test based on the testIterator
        :return: Void
        """
        #self.checkThreadTimer.stop()
        self.tests[self.testIterator].run()

        self.testIterator = self.testIterator + 1

        if(self.testIterator == len(self.tests)):
            self.testIterator = 0
            self.checkThreadTimer.timeout.disconnect(self.runTests)
            self.checkThreadTimer.timeout.connect(self.checkTests)
            self.checkThreadTimer.start()
            return

        self.checkThreadTimer.start()

    def checkTests(self):
        #self.checkThreadTimer.stop()
        self.webView.setHtml("<h1>Verifying Test(s)...</h1>")
        self.listView.update()

        self.tests[self.testIterator].assertMatchingCounts()

        self.testIterator = self.testIterator + 1
        if (self.testIterator == len(self.tests)):
            self.testIterator = 0
            self.checkThreadTimer.stop()
            self.webView.setHtml("<h1>Tests Checked<br/> Select a test to view its description.</h1>")
            self.update()
            return

        self.checkThreadTimer.start()


#will be used to populate the list view in the TestExplorer (list of Test)
class ItemListModel(QAbstractListModel):
    def __init__(self, datain, parent=None, *args):
        """ datain: a list where each item is a row
        """
        QAbstractListModel.__init__(self, parent, *args)
        self.listData = datain #from here on out, listData holds all the data that was used to instantiate this class

    def rowCount(self, parent=QModelIndex()):
        return len(self.listData)

    def data(self, index, role):
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(self.listData[index.row()].name)
        elif role == Qt.DecorationRole:
            button = QPushButton("Test")
            style = button.style()
            #set the icon based on the status of the item
            icon = style.standardIcon(QStyle.SP_MessageBoxQuestion)
            status = self.listData[index.row()].status
            if ( status == TestStatus.Passed): #if the test passed
                icon = style.standardIcon(QStyle.SP_DialogApplyButton)
            elif ( status == TestStatus.Executing):
                icon = style.standardIcon(QStyle.SP_MediaPlay)
            elif ( status == TestStatus.Failed): #if the test failed
                icon = style.standardIcon(QStyle.SP_DialogCancelButton)
            return icon
        else:
            return QVariant()