# This file is incomplete. Will house the user Worth Summary broken down by existing accounts

import sys
import sqlite3

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFrame, QScrollArea, QWidget, QGridLayout,\
    QVBoxLayout, QLabel, QSizePolicy, QSpacerItem, QProgressBar
from PyQt5.QtCore import pyqtSlot
from sqlite3 import Error

from Frontend.SummaryUi import Ui_Dialog
from Backend.UPK import add_comma, decimal_places, modify_for_sql, obtain_sql_value, obtain_sql_list, set_font
from Frontend.StyleSheets import messagesheet, innerframesheet, progressSheet, parentypeSheet, colheadersheet, subtotalsheet,\
    accountsheet
from Backend.Graphing import nested_snapshot, AF_Canvas


class LedgerS(QDialog):
    remove_tab_LS = QtCore.pyqtSignal(str)

    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    def __init__(self, parent, database, dataCheck):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.refUserDB = database
        self.summaryTuple = None
        # label dictionary[AccountName] = label for Account Balances
        self.balancelabeldic = {}
        # label dictionary[ParentType] = label for SubType Balances
        self.subtotaldic = {}
        # label dictionary[AccountName] = label for ProgressBar
        self.progBardic = {}
        self.updateMessages = []

        # --- Frame Creation for the Graphs ---------------------------------------------------------------------------------------------
        self.assetlabel = QLabel(self)
        self.assetlabel.setGeometry(20, 10, 410, 40)
        self.assetlabel.setText("Asset Distribution")
        graphfont = QtGui.QFont()
        set_font(graphfont, 16, True, 70, False)
        self.set_formatting(self.assetlabel, graphfont, QtCore.Qt.AlignCenter, parentypeSheet)

        self.assetCanvas = AF_Canvas(self, width=5, height=4, dpi=200)
        self.assetFrame = QFrame(self)
        self.assetFrame.setGeometry(20, 55, 410, 310)
        self.assetFrame.setMaximumWidth(410)
        self.assetFrame.setFrameStyle(1)

        self.assetLayout = QVBoxLayout(self.assetFrame)
        self.assetLayout.addWidget(self.assetCanvas)
        self.update_plot(focus="Asset", canvas=self.assetCanvas)

        # --- Frame Creation for Liability Graph ------------------------------------------------------------------------------------------
        self.liabilitylabel = QLabel(self)
        self.liabilitylabel.setGeometry(20, 395, 410, 40)
        self.liabilitylabel.setText("Liability Distribution")
        set_font(graphfont, 16, True, 70, False)
        self.set_formatting(self.liabilitylabel, graphfont, QtCore.Qt.AlignCenter, parentypeSheet)

        self.liabilityCanvas = AF_Canvas(self, width=5, height=4, dpi=200)
        self.liabilityFrame = QFrame(self)
        self.liabilityFrame.setGeometry(20, 440, 410, 310)
        self.liabilityFrame.setMaximumWidth(410)
        self.liabilityFrame.setFrameStyle(1)

        self.liabilityLayout = QVBoxLayout(self.liabilityFrame)
        self.liabilityLayout.addWidget(self.liabilityCanvas)
        self.update_plot(focus="Liability", canvas=self.liabilityCanvas)

        # Label Below exists as a method of checking that data was transferring between modules properly.
        # self.ui.labelTest.setText(dataCheck)
        self.ui.labelTest.hide()

        # --- Frame Creation for the Summary Chart -------------------------------------------------------------------------------------
        self.summaryFrame = QFrame(self)
        self.summaryFrame.setGeometry(450, 0, 750, 801)
        # self.summaryFrame.setMaximumWidth(750)
        self.summaryFrame.setMaximumSize(750, 801)
        self.summaryFrame.setFrameStyle(1)

        self.obtain_summaryTuple()
        self.summaryScroll = QScrollArea(self.summaryFrame)
        self.summaryScroll.setGeometry(0, 0, 700, 801)
        self.summaryScroll.setFixedWidth(750)
        self.summaryScroll.horizontalScrollBar().setEnabled(False)
        self.summaryScroll.setFixedHeight(780)
        self.summaryScroll.setFrameStyle(0)
        self.summaryScroll.setWidgetResizable(True)

        widget = QWidget()
        widget.setMaximumWidth(730)
        self.summaryScroll.setWidget(widget)
        self.layout_SArea = QVBoxLayout(widget)
        self.layout_SArea.addWidget(self.generate_layout())
        self.layout_SArea.addStretch(1)
        self.setStyleSheet(progressSheet)
        self.show()

        # parent.refresh_signal_summary.connect(self.refresh_balance_labels)
        parent.refresh_signal_summary.connect(self.refresh_summary)

    def obtain_summaryTuple(self):
        summaryStatement = """SELECT ItemType, ParentType, SubType, ID, Balance FROM Account_Summary """ \
                           + """ORDER BY "ItemType", "ParentType", "SubType", "Balance" DESC LIMIT 0, 49999"""
        try:
            conn = sqlite3.connect(self.refUserDB)
            with conn:
                cur = conn.cursor()
                cur.execute(summaryStatement)
                summaryDate = cur.fetchall()
                self.summaryTuple = summaryDate
        except Error:
            print("Error Summary Data Collection Failure")
        finally:
            conn.close()

    # def set_font(self, target, size, bold, weight, underline):
    #     target.setPointSize(size)
    #     target.setBold(bold)
    #     target.setWeight(weight)
    #     target.setUnderline(underline)

    def set_formatting(self, target, font, Alignment, stylesheet):
        target.setFont(font)
        target.setFrameShape(QFrame.Panel)
        target.setFrameShadow(QFrame.Sunken)
        target.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | Alignment)
        target.setStyleSheet(stylesheet)

    def generate_layout(self):
        innerFrame = QFrame(self)
        innerFrame.setStyleSheet(innerframesheet)
        summarygridLayout = QGridLayout(innerFrame)

        horizontalSpacer = QSpacerItem(100, 20, QSizePolicy.Fixed, QSizePolicy.Expanding)
        # (row, col, rowspn columnspan)
        summarygridLayout.addItem(horizontalSpacer, 0, 0, 1, 1)

        spacerLabel = QLabel(self)
        spacerLabel.setObjectName("SpacerLabel")
        spacerLabel.setText("")
        spacerLabel.setFixedWidth(250)
        summarygridLayout.addWidget(spacerLabel, 1, 4, 1, 1)

        row = 0
        subTotal = 0

        listofBank = [account for account in self.summaryTuple if "Bank" in account]
        listofCD = [account for account in self.summaryTuple if "CD" in account]
        listofCash = [account for account in self.summaryTuple if "Cash" in account]
        listofEquity = [account for account in self.summaryTuple if "Equity" in account]
        listofRetirement = [account for account in self.summaryTuple if "Retirement" in account]
        listofCredit = [account for account in self.summaryTuple if "Credit" in account]
        listofDebt = [account for account in self.summaryTuple if "Debt" in account]
        listofTreasury = [account for account in self.summaryTuple if "Treasury" in account]

        parentType_dict = {
            "Bank": listofBank,
            "Cash": listofCash,
            "Certificate of Deposit": listofCD,
            "Equity": listofEquity,
            "Treasury Bonds": listofTreasury,
            "Retirement": listofRetirement,
            "Credit": listofCredit,
            "Debt": listofDebt
        }

        labelMessage = QLabel(self)
        labelMessage.setObjectName("labelMessages")
        labelMessage.setText("")
        messagefont = QtGui.QFont()
        set_font(messagefont, 12, True, 50, False)
        labelMessage.setFont(messagefont)
        labelMessage.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        labelMessage.setFrameShape(QFrame.Panel)
        labelMessage.setFrameShadow(QFrame.Plain)
        summarygridLayout.addWidget(labelMessage, row, 0, 1, 4)
        labelMessage.hide()
        self.updateMessages.append(labelMessage)

        row += 1

        for parentType in parentType_dict:
            listofAccounts = parentType_dict[parentType]
            if len(listofAccounts) > 0:
                labelparent = QLabel(self)
                labelparent.setObjectName("label" + parentType)
                labelparent.setText("  " + parentType.title())
                parentfont = QtGui.QFont()
                set_font(parentfont, 16, True, 70, False)
                self.set_formatting(labelparent, parentfont, QtCore.Qt.AlignLeft, parentypeSheet)
                summarygridLayout.addWidget(labelparent, row, 0, 1, 4)

                row += 1

                labelColheader1 = QLabel(self)
                labelColheader1.setObjectName("labelAN" + parentType + "header")
                labelColheader1.setText("Account Name")
                headerfont = QtGui.QFont()
                set_font(headerfont, 10, True, 60, False)
                self.set_formatting(labelColheader1, headerfont, QtCore.Qt.AlignHCenter, colheadersheet)
                summarygridLayout.addWidget(labelColheader1, row, 1, 1, 1)

                labelColheader2 = QLabel(self)
                labelColheader2.setObjectName("labelAT" + parentType + "header")
                labelColheader2.setText("Account Type")
                self.set_formatting(labelColheader2, headerfont, QtCore.Qt.AlignHCenter, colheadersheet)
                summarygridLayout.addWidget(labelColheader2, row, 2, 1, 1)

                labelColheader3 = QLabel(self)
                labelColheader3.setObjectName("labelB" + parentType + "header")
                labelColheader3.setText("Balance")
                self.set_formatting(labelColheader3, headerfont, QtCore.Qt.AlignHCenter, colheadersheet)
                summarygridLayout.addWidget(labelColheader3, row, 3, 1, 1)

                row += 1

                for account in listofAccounts:
                    # [A/L, ParentType, Subtype, ID, Balance]
                    accountID = modify_for_sql(account[3])
                    verticalSpacer = QSpacerItem(80, 40, QSizePolicy.Fixed, QSizePolicy.Minimum)
                    summarygridLayout.addItem(verticalSpacer, row, 0, 1, 1)

                    labelID = QLabel(self)
                    labelID.setObjectName("labelAN" + accountID)
                    labelID.setText("  " + account[3].title() + "     ")
                    IDfont = QtGui.QFont()
                    set_font(IDfont, 10, False, 50, False)
                    labelID.setFont(IDfont)
                    labelID.setStyleSheet(accountsheet)
                    summarygridLayout.addWidget(labelID, row, 1, 1, 1)

                    labelSubtype = QLabel(self)
                    labelSubtype.setObjectName("labelAT" + accountID)
                    labelSubtype.setText("  " + account[2].title())
                    subtypeFont = QtGui.QFont()
                    set_font(subtypeFont, 10, False, 50, False)
                    labelSubtype.setFont(subtypeFont)
                    labelSubtype.setAlignment(QtCore.Qt.AlignVCenter|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
                    labelSubtype.setStyleSheet(accountsheet)
                    summarygridLayout.addWidget(labelSubtype, row, 2, 1, 1)

                    labelBalance = QLabel(self)
                    labelBalance.setObjectName("labelBal" + accountID)
                    # label dictionary[AccountName] = labelBalance for Account Balances
                    self.balancelabeldic[account[3]] = labelBalance

                    if account[0] == "Liability":
                        raw_Balance = - account[4]
                    else:
                        raw_Balance = account[4]

                    modBalance = decimal_places(raw_Balance, 2)
                    subTotal += modBalance
                    with_comma = add_comma(modBalance, 2)

                    if modBalance > 0:
                        labelBalance.setText("  $  " + with_comma + "     ")
                    elif modBalance == 0:
                        labelBalance.setText("  $  0.00     ")
                    else:
                        labelBalance.setText("  ($  " + with_comma + ")     ")

                    labelBalance.setFont(IDfont)
                    labelBalance.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeading | QtCore.Qt.AlignRight)
                    labelBalance.setStyleSheet(accountsheet)
                    summarygridLayout.addWidget(labelBalance, row, 3, 1, 1)

                    row += 1

                    if parentType == "Debt" or parentType == "Credit":
                        labelprogress = QLabel(self)
                        labelprogress.setObjectName("labelProg" + accountID)
                        if parentType == "Debt":
                            labelprogress.setText("  Percent Remaining:")
                        else:
                            labelprogress.setText("  Credit Available:")
                        progressfont = QtGui.QFont()
                        set_font(progressfont, 8, True, 65, False)
                        labelprogress.setFont(progressfont)
                        labelprogress.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeading | QtCore.Qt.AlignRight)
                        summarygridLayout.addWidget(labelprogress, row, 1, 1, 1)

                        debtprogressBar = QProgressBar(self)
                        debtprogressBar.setMinimum(0)
                        debtprogressBar.setMaximum(100)

                        if parentType == "Debt":
                            start = self.obtain_liability_start("Starting_Balance", "Debt_Account_Details", account[3])
                            progress = (decimal_places(account[4], 2) / decimal_places(start, 2)) * 100
                            progress = int(progress)
                        else:
                            start = self.obtain_liability_start("Credit_Limit", "Credit_Account_Details", account[3])
                            progress = 100 - ((decimal_places(account[4], 2) / decimal_places(start, 2)) * 100)
                            progress = int(progress)

                        debtprogressBar.setProperty("value", progress)
                        debtprogressBar.setObjectName("progressBar" + accountID)
                        # label dictionary[AccountName] = label for ProgressBar
                        self.progBardic[account[3]] = debtprogressBar
                        summarygridLayout.addWidget(debtprogressBar, row, 2, 1, 2)

                    row += 1

                labelTotal = QLabel(self)
                labelTotal.setObjectName("label" + parentType + "total")
                labelTotal.setText("Subtotal")
                totalfont = QtGui.QFont()
                set_font(totalfont, 8, True, 65, False)
                labelTotal.setFont(totalfont)
                labelTotal.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeading | QtCore.Qt.AlignRight)
                summarygridLayout.addWidget(labelTotal, row, 1, 1, 2)

                labelSubTotal = QLabel(self)
                labelSubTotal.setObjectName("label" + parentType + "Subtotal")
                # label dictionary[ParentType] = label for SubType Balances
                self.subtotaldic[parentType] = labelSubTotal
                subTotal = decimal_places(subTotal, 2)
                subTotal = add_comma(subTotal, 2)
                if parentType == "Debt" or parentType == "Credit":
                    labelSubTotal.setText("  ($  " + subTotal + ")    ")
                else:
                    labelSubTotal.setText("  $  " + subTotal + "    ")
                labelSubTotal.setFont(IDfont)
                labelSubTotal.setFrameShape(QFrame.Panel)
                labelSubTotal.setFrameShadow(QFrame.Sunken)
                labelSubTotal.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeading | QtCore.Qt.AlignRight)
                labelSubTotal.setStyleSheet(subtotalsheet)
                summarygridLayout.addWidget(labelSubTotal, row, 3, 1, 1)

                row += 1
                subTotal = 0
            else:
                pass
        return innerFrame

    def obtain_liability_start(self, col, tableName, accountName):
        startStatement = "SELECT " + col + " FROM " + tableName + " WHERE Account_Name='" + accountName + "'"
        try:
            conn = sqlite3.connect(self.refUserDB)
            with conn:
                cur = conn.cursor()
                cur.execute(startStatement)
                start = cur.fetchone()
        except Error:
            start = 0.00
            return start
        finally:
            conn.close()
            start = start[0]
        return start

    def refresh_balance_labels(self):
        for account in self.balancelabeldic:
            balanceStatement = "SELECT Balance, ItemType, ParentType FROM Account_Summary WHERE ID='" + account + "'"
            accountInfo = obtain_sql_value(balanceStatement, self.refUserDB)
            if accountInfo is None:
                accountInfo = (0.00, "Deleted", "Deleted")
            modBalance = add_comma(accountInfo[0],  2)
            targetlabel = self.balancelabeldic[account]

            if accountInfo[1] == "Liability":
                if accountInfo[0] >= 0:
                    targetlabel.setText("  ($  " + modBalance + ")     ")
                else:
                    targetlabel.setText("  $  " + modBalance + "     ")
            elif accountInfo[1] == "Deleted":
                targetlabel.setText("$ 0.00")
            else:
                if accountInfo[0] >= 0:
                    targetlabel.setText("  $  " + modBalance + "     ")
                else:
                    targetlabel.setText("  ($  " + modBalance + ")     ")

            if account in self.progBardic:
                if accountInfo[2] == "Debt":
                    start = self.obtain_liability_start("Starting_Balance", "Debt_Account_Details", account)
                    progress = (decimal_places(accountInfo[0], 2) / decimal_places(start, 2)) * 100
                    progress = int(progress)
                    targetbar = self.progBardic[account]
                    targetbar.setProperty("value", progress)
                elif accountInfo[2] == "Deleted":
                    progress = 100
                    targetbar = self.progBardic[account]
                    targetbar.setProperty("value", progress)
                else:
                    start = self.obtain_liability_start("Credit_Limit", "Credit_Account_Details", account)
                    progress = 100 - ((decimal_places(accountInfo[0], 2) / decimal_places(start, 2)) * 100)
                    progress = int(progress)
                    targetbar = self.progBardic[account]
                    targetbar.setProperty("value", progress)

        for parentType in self.subtotaldic:
            if parentType == "Certificate of Deposit":
                sqlparentType = "CD"
            elif parentType == "Treasury Bonds":
                sqlparentType = "Treasury"
            else:
                sqlparentType = parentType
            subTotalStatement = "SELECT SUM(Balance), ItemType FROM Account_Summary WHERE ParentType='" + sqlparentType + "'"
            subTotalInfo = obtain_sql_value(subTotalStatement, self.refUserDB)
            preModSubTotal = subTotalInfo[0]

            if preModSubTotal is None:
                preModSubTotal = 0.0

            if subTotalInfo[1] == "Liability":
                raw_Balance = - preModSubTotal
            else:
                raw_Balance = preModSubTotal

            modBalance = decimal_places(raw_Balance, 2)
            modSubTotal = add_comma(modBalance, 2)
            targetlabel = self.subtotaldic[parentType]

            if modBalance > 0:
                targetlabel.setText("  $  " + modSubTotal + "    ")
            elif modBalance == 0:
                targetlabel.setText("$  0.00     ")
            else:
                targetlabel.setText("  ($  " + modSubTotal + ")    ")

    def user_messages(self):
        accountStatment = "SELECT ID FROM Account_Summary"
        accountList = obtain_sql_list(accountStatment, self.refUserDB)
        currentQTYaccounts = len(accountList)
        oldQTYaccounts = len(self.summaryTuple)
        messagelabel = self.updateMessages[0]
        messagelabel.setStyleSheet(messagesheet)

        changes = "Reload to Display Changes to Accounts"

        if currentQTYaccounts != oldQTYaccounts:
            messagelabel.setText(changes)
            messagelabel.show()

    def update_plot(self, focus, canvas):
        pie_data = nested_snapshot(self.refUserDB, graph_focus=focus)
        canvas.axes.clear()
        canvas.axes.pie(pie_data[0], radius=1.5, colors=pie_data[1], wedgeprops={'linewidth': 0.5, 'edgecolor': 'grey', 'width': 0.3})
        canvas.axes.pie(pie_data[2], radius=1.2, colors=pie_data[3], wedgeprops={'linewidth': 0.3, 'edgecolor': 'grey', 'width': 0.25})
        if focus == "Asset":
            assetSizes = pie_data[4]
            LegendLabels = ["Bank - ({0}%)".format(assetSizes[0]),
                            "Cash - ({0}%)".format(assetSizes[1]),
                            "CD - ({0}%)".format(assetSizes[2]),
                            "Equity - ({0}%)".format(assetSizes[3]),
                            "Treasury - ({0}%)".format(assetSizes[4]),
                            "Retirement - ({0}%)".format(assetSizes[5])]

        elif focus == "Liability":
            liabilitySizes = pie_data[4]
            LegendLabels = ["Debt - ({0}%)".format(liabilitySizes[0]),
                            "Credit - ({0}%)".format(liabilitySizes[1])]
        else:
            LegendLabels = ["Input Error: Asset/Liability only"]

        canvas.axes.legend(
            loc="center",
            labels=LegendLabels,
            ncol=1,
            fontsize=3.5,
            bbox_to_anchor=(0.52, 0.5),
            frameon=False,
        )
        canvas.draw()

    # --- Receive a message from the MainWindow to refresh -----------------------
    @pyqtSlot(str)
    def refresh_summary(self, message):
        if message == "2":
            self.update_plot("Asset", self.assetCanvas)
            self.update_plot("Liability", self.liabilityCanvas)
            self.refresh_balance_labels()
            self.user_messages()
        else:
            print("Failure Summary 423")

    # --- PyQt5 signal to remove ParentType Ledger from tabdic ---------------------------------------------------------
    def trigger_del_tab(self):
        self.remove_tab_LS.emit("Summary")

    def closeEvent(self, event):
        event.ignore()
        self.trigger_del_tab()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    lily = LedgerS()
    lily.show()
    sys.exit(app.exec_())
