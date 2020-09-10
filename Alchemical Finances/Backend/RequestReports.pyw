import sys
import os

from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5 import QtCore, QtWidgets


from Frontend.GenerateReportsUi import Ui_Dialog
from Frontend.StyleSheets import UniversalStyleSheet
from Backend.BuildReports import Generate_user_report


class user_report_request(QDialog):

    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    def __init__(self, database, user):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Request Summary Report")
        self.setStyleSheet(UniversalStyleSheet)
        self.setModal(True)
        self.show()

        # --- Class Global Variables ------------------------------------------------------------------------------------------------------------------------------------------
        self.refUserDB = database
        self.refUser = user

        self.widgetlist = [
            self.ui.checkBoxBank,
            self.ui.checkBoxCash,
            self.ui.checkBoxCD,
            self.ui.checkBoxCredit,
            self.ui.checkBoxEquity,
            self.ui.checkBoxRetirement,
            self.ui.checkBoxTreasury,
            self.ui.checkBoxDebt,
        ]

        self.parentType = {
            self.ui.checkBoxBank: "Bank",
            self.ui.checkBoxCash: "Cash",
            self.ui.checkBoxCD: "CD",
            self.ui.checkBoxEquity: "Equity",
            self.ui.checkBoxRetirement: "Retirement",
            self.ui.checkBoxTreasury: "Treasury",
            self.ui.checkBoxDebt: "Debt",
            self.ui.checkBoxCredit: "Credit",

        }

        # --- Main Program ----------------------------------------------------------------------------------------------------------------------------------------------------
        self.ui.pushButtonDeselect.clicked.connect(lambda: self.select_checkboxes(False))
        self.ui.pushButtonSelectAll.clicked.connect(lambda: self.select_checkboxes(True))
        self.ui.pushButtonPrint.clicked.connect(lambda: self.generate_list(self.ui.lineEditPathway.text()))
        self.ui.pushButtonFile.clicked.connect(self.obtain_user_dir)

        self.ui.label.setText("Report Destination")

        initial_dir = os.path.join(os.path.expanduser("~"), "Documents/")
        self.ui.lineEditPathway.setText(initial_dir)

    # --- Functions -----------------------------------------------------------------------------------------------------------------------------------------------------------
    # --- -- Used to Select all and Deselect all checkbox options -------------------------------------------------------------------------------------------------------------
    def select_checkboxes(self, state):
        for widget in self.widgetlist:
            widget.setChecked(state)

    # --- -- Obtain user input directory --------------------------------------------------------------------------------------------------------------------------------------
    def obtain_user_dir(self):
        dirname = QFileDialog.getExistingDirectory(self, "Chose Destination", os.getcwd(), QFileDialog.ShowDirsOnly)
        if dirname:
            self.ui.lineEditPathway.setText(dirname)
        else:
            dirname = os.path.join(os.path.expanduser("~"), "Documents/")
            self.ui.lineEditPathway.setText(dirname)

    # --- -- Used to Generate the report and open the .pdf file ---------------------------------------------------------------------------------------------------------------
    def generate_list(self, directory):
        request = []
        for widget in self.widgetlist:
            if widget.checkState() == 2:
                parenType_request = [self.parentType[widget], "", ""]
                request.append(parenType_request)

        input_Data = [self.refUserDB, self.refUser, request, directory]
        Generate_user_report(input_Data)
        self.close()

    def closeEvent(self, event):
        event.ignore()
        self.accept()


if __name__ == "__main__":
    database = os.path.join(os.getcwd(), '..', 'data/account/b8aem6j45m5r36ghs.db')
    app = QApplication(sys.argv)
    lily = user_report_request(database, "Jmshamberg")
    lily.show()
    sys.exit(app.exec_())
