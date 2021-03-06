# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AlchemicalFinancesUi.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 900)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1200, 900))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        MainWindow.setWindowIcon(QtGui.QIcon('AF Logo.png'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mdiArea = QtWidgets.QMdiArea(self.centralwidget)
        self.mdiArea.setEnabled(True)
        self.mdiArea.setGeometry(QtCore.QRect(0, 50, 1200, 801))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mdiArea.sizePolicy().hasHeightForWidth())
        self.mdiArea.setSizePolicy(sizePolicy)
        self.mdiArea.setActivationOrder(QtWidgets.QMdiArea.StackingOrder)
        self.mdiArea.setViewMode(QtWidgets.QMdiArea.TabbedView)
        self.mdiArea.setTabsClosable(True)
        self.mdiArea.setTabsMovable(True)
        self.mdiArea.setObjectName("mdiArea")
        self.labelNW = QtWidgets.QLabel(self.centralwidget)
        self.labelNW.setGeometry(QtCore.QRect(975, 0, 225, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelNW.setFont(font)
        self.labelNW.setText("")
        self.labelNW.setAlignment(QtCore.Qt.AlignCenter)
        self.labelNW.setObjectName("labelNW")
        self.labelStaticNW = QtWidgets.QLabel(self.centralwidget)
        self.labelStaticNW.setGeometry(QtCore.QRect(835, 0, 140, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelStaticNW.setFont(font)
        self.labelStaticNW.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelStaticNW.setObjectName("labelStaticNW")
        self.labelStaticNTD = QtWidgets.QLabel(self.centralwidget)
        self.labelStaticNTD.setGeometry(QtCore.QRect(470, 0, 140, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelStaticNTD.setFont(font)
        self.labelStaticNTD.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelStaticNTD.setObjectName("labelStaticNTD")
        self.labelTD = QtWidgets.QLabel(self.centralwidget)
        self.labelTD.setGeometry(QtCore.QRect(600, 0, 225, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelTD.setFont(font)
        self.labelTD.setText("")
        self.labelTD.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTD.setObjectName("labelTD")
        self.labelStaticTA = QtWidgets.QLabel(self.centralwidget)
        self.labelStaticTA.setGeometry(QtCore.QRect(105, 0, 140, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelStaticTA.setFont(font)
        self.labelStaticTA.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelStaticTA.setObjectName("labelStaticTA")
        self.labelTA = QtWidgets.QLabel(self.centralwidget)
        self.labelTA.setGeometry(QtCore.QRect(245, 0, 225, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelTA.setFont(font)
        self.labelTA.setText("")
        self.labelTA.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTA.setObjectName("labelTA")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 18))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAssets = QtWidgets.QMenu(self.menubar)
        self.menuAssets.setObjectName("menuAssets")
        self.menuLiabilities = QtWidgets.QMenu(self.menubar)
        self.menuLiabilities.setObjectName("menuLiabilities")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionSummary = QtWidgets.QAction(MainWindow)
        self.actionSummary.setObjectName("actionSummary")
        self.actionProfile = QtWidgets.QAction(MainWindow)
        self.actionProfile.setObjectName("actionProfile")
        self.actionExport = QtWidgets.QAction(MainWindow)
        self.actionExport.setObjectName("actionExport")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionBank = QtWidgets.QAction(MainWindow)
        self.actionBank.setObjectName("actionBank")
        self.actionEquity = QtWidgets.QAction(MainWindow)
        self.actionEquity.setObjectName("actionEquity")
        self.actionCertificate_of_Deposit = QtWidgets.QAction(MainWindow)
        self.actionCertificate_of_Deposit.setObjectName("actionCertificate_of_Deposit")
        self.actionRetirement = QtWidgets.QAction(MainWindow)
        self.actionRetirement.setObjectName("actionRetirement")
        self.actionTreasury_Bonds = QtWidgets.QAction(MainWindow)
        self.actionTreasury_Bonds.setObjectName("actionTreasury_Bonds")
        self.actionDebt = QtWidgets.QAction(MainWindow)
        self.actionDebt.setObjectName("actionDebt")
        self.actionCredit_Cards = QtWidgets.QAction(MainWindow)
        self.actionCredit_Cards.setObjectName("actionCredit_Cards")
        self.actionCash = QtWidgets.QAction(MainWindow)
        self.actionCash.setObjectName("actionCash")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionUserManual = QtWidgets.QAction(MainWindow)
        self.actionUserManual.setObjectName("actionUserManual")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionArchive = QtWidgets.QAction(MainWindow)
        self.actionArchive.setObjectName("actionArchive")
        self.actionReports_Future = QtWidgets.QAction(MainWindow)
        self.actionReports_Future.setObjectName("actionReports_Future")
        self.actionBudgeting_Future = QtWidgets.QAction(MainWindow)
        self.actionBudgeting_Future.setObjectName("actionBudgeting_Future")
        self.actionGenerate = QtWidgets.QAction(MainWindow)
        self.actionGenerate.setObjectName("actionGenerate")
        self.actionNWG = QtWidgets.QAction(MainWindow)
        self.actionNWG.setObjectName("actionNWG")
        self.menuFile.addAction(self.actionSummary)
        self.menuFile.addAction(self.actionGenerate)
        self.menuFile.addAction(self.actionNWG)
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionClose)
        self.menuAssets.addAction(self.actionBank)
        self.menuAssets.addAction(self.actionCash)
        self.menuAssets.addAction(self.actionCertificate_of_Deposit)
        self.menuAssets.addAction(self.actionEquity)
        self.menuAssets.addAction(self.actionRetirement)
        self.menuAssets.addAction(self.actionTreasury_Bonds)
        self.menuLiabilities.addAction(self.actionDebt)
        self.menuLiabilities.addAction(self.actionCredit_Cards)
        self.menuTools.addAction(self.actionArchive)
        self.menuTools.addAction(self.actionReports_Future)
        self.menuTools.addAction(self.actionBudgeting_Future)
        self.menuAbout.addAction(self.actionUserManual)
        self.menuAbout.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAssets.menuAction())
        self.menubar.addAction(self.menuLiabilities.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Alchemical Finances"))
        self.labelStaticNW.setText(_translate("MainWindow", "Net Worth:"))
        self.labelStaticNTD.setText(_translate("MainWindow", "Total Debt:"))
        self.labelStaticTA.setText(_translate("MainWindow", "Total Assets:"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAssets.setTitle(_translate("MainWindow", "Assets"))
        self.menuLiabilities.setTitle(_translate("MainWindow", "Liabilities"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.menuAbout.setTitle(_translate("MainWindow", "Other"))
        self.actionSummary.setText(_translate("MainWindow", "Summary"))
        self.actionProfile.setText(_translate("MainWindow", "Profile [Future]"))
        self.actionExport.setText(_translate("MainWindow", "Export [Future]"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionBank.setText(_translate("MainWindow", "Bank"))
        self.actionEquity.setText(_translate("MainWindow", "Equity"))
        self.actionEquity.setToolTip(_translate("MainWindow", "Equity"))
        self.actionCertificate_of_Deposit.setText(_translate("MainWindow", "Certificate of Deposit"))
        self.actionRetirement.setText(_translate("MainWindow", "Retirement"))
        self.actionRetirement.setToolTip(_translate("MainWindow", "Retirement"))
        self.actionTreasury_Bonds.setText(_translate("MainWindow", "Treasury Bonds"))
        self.actionDebt.setText(_translate("MainWindow", "Debt"))
        self.actionCredit_Cards.setText(_translate("MainWindow", "Credit Cards"))
        self.actionCash.setText(_translate("MainWindow", "Cash"))
        self.actionSave.setText(_translate("MainWindow", "Save [Future]"))
        self.actionUserManual.setText(_translate("MainWindow", "User Manual"))
        self.actionUserManual.setToolTip(_translate("MainWindow", "User Manual"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setToolTip(_translate("MainWindow", "Other"))
        self.actionArchive.setText(_translate("MainWindow", "Archive"))
        self.actionReports_Future.setText(_translate("MainWindow", "Reports [Future]"))
        self.actionBudgeting_Future.setText(_translate("MainWindow", "Budgeting [Future]"))
        self.actionGenerate.setText(_translate("MainWindow", "Generate Report"))
        self.actionNWG.setText(_translate("MainWindow", "Net Worth Graph"))


