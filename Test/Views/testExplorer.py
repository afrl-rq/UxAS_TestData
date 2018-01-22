from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Views.statusView import StatusView

#will be used to populate the list view in the TestExplorer (list of Test)
class ItemListModel(QAbstractListModel):
    def __init__(self, datain, parent=None, *args):
        """ datain: a list where each item is a row
        """
        QAbstractListModel.__init__(self, parent, *args)
        self.listData = datain # listData holds all the data that was used to instantiate this class


    def rowCount(self, parent=QModelIndex()):
        return len(self.listData)

    def data(self, index, role):
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(self.listData[index.row()].name)
        elif role == Qt.DecorationRole:
            button = QPushButton("Test")
            style = button.style()
            icon = style.standardIcon(QStyle.SP_DialogApplyButton)
            if(not self.listData[index.row()].isValidTest()):
                icon = style.standardIcon(QStyle.SP_MessageBoxWarning)
            return icon
        else:
            return QVariant()


# A class that will hold the UI for the test explorer
class TestExplorer(QDialog):
    # initializer for the TestExplorer. Before initialized, the tests should all be created at this point and passed into the TestExplorer
    def __init__(self, applicableTests):
        QDialog.__init__(self)  # call constructor of parent class
        self.applicableTests = applicableTests  # hang on to those tests. They're needed to run the selected tests
        self.statusView = None

        # set the layout
        layout = QGridLayout()  # put everything in the layout in a grid
        self.setWindowTitle("TestExplorer")

        ######################################################################
        #                        SETUP THE WIDGETS                          #
        ######################################################################

        # add a run all tests widget
        runAllButton = QPushButton("Select All")
        runAllButton.clicked.connect(self.selectAllButton_Clicked)

        # add a run selected tests widget
        runSelectedButton = QPushButton("Run Selected Tests")
        runSelectedButton.clicked.connect(self.runButton_Clicked)

        # add a cancel (close window) widget
        cancelButton = QPushButton("Cancel")
        cancelButton.clicked.connect(self.cancelButton_Clicked)

        # Create list view
        self.lm = ItemListModel(applicableTests, self)

        self.lv = QListView()
        self.lv.setModel(self.lm)
        self.lv.setSelectionMode( QAbstractItemView.ExtendedSelection )


        ######################################################################
        #                         SETUP THE LAYOUT                           #
        ######################################################################

        layout.addWidget(self.lv, 0,0)
        # add the buttons to the layout
        layout.addWidget(runAllButton, 1, 0)
        layout.addWidget(runSelectedButton, 2, 0)
        layout.addWidget(cancelButton, 3, 0)

        self.setLayout(layout)

    ######################################################################
    #                SOME HANDLERS FOR THE WIDGET EVENTS                 #
    ######################################################################

    def selectAllButton_Clicked(self):
        """Selects all tests in the view
        """
        self.lv.selectAll()

    def runButton_Clicked(self):
        """Runs the selected tests in the view
        """
        indices = self.lv.selectedIndexes()

        if not indices:
            return

        validTests = [self.lm.listData[index.row()] for index in indices if (self.lm.listData[index.row()].isValidTest())]

        #show warning box if the selected tests are not valid
        if not validTests:
            warningBox = QMessageBox()
            warningBox.setIcon(QMessageBox.Warning)
            warningBox.setWindowTitle("Warning")
            warningBox.setText("Warning!")
            warningBox.setInformativeText("The selected tests are not valid. Check if they have an accepted database and a test script.")
            warningBox.exec_()
            return

        self.statusView = StatusView(validTests)
        self.statusView.exec_()

    def cancelButton_Clicked(self):
        """Closes the view
        """
        self.close()