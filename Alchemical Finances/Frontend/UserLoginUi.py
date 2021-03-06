# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UserLoginUi.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(345, 311)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMaximumSize(QtCore.QSize(450, 420))
        Dialog.setWindowIcon(QtGui.QIcon('AF Logo.png'))
        self.labelUserProfile = QtWidgets.QLabel(Dialog)
        self.labelUserProfile.setGeometry(QtCore.QRect(20, 100, 141, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelUserProfile.setFont(font)
        self.labelUserProfile.setObjectName("labelUserProfile")
        self.labelPassword = QtWidgets.QLabel(Dialog)
        self.labelPassword.setGeometry(QtCore.QRect(20, 130, 141, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelPassword.setFont(font)
        self.labelPassword.setObjectName("labelPassword")
        self.lineEditUserProfile = QtWidgets.QLineEdit(Dialog)
        self.lineEditUserProfile.setGeometry(QtCore.QRect(170, 100, 150, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEditUserProfile.setFont(font)
        self.lineEditUserProfile.setObjectName("lineEditUserProfile")
        self.lineEditPassword = QtWidgets.QLineEdit(Dialog)
        self.lineEditPassword.setGeometry(QtCore.QRect(170, 130, 150, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEditPassword.setFont(font)
        self.lineEditPassword.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.lineEditPassword.setObjectName("lineEditPassword")
        self.pushButtonLogin = QtWidgets.QPushButton(Dialog)
        self.pushButtonLogin.setGeometry(QtCore.QRect(65, 200, 100, 25))
        self.pushButtonLogin.setObjectName("pushButtonLogin")
        self.pushButtonQuit = QtWidgets.QPushButton(Dialog)
        self.pushButtonQuit.setGeometry(QtCore.QRect(175, 200, 100, 25))
        self.pushButtonQuit.setObjectName("pushButtonQuit")
        self.pushButtonNewProfile = QtWidgets.QPushButton(Dialog)
        self.pushButtonNewProfile.setGeometry(QtCore.QRect(65, 230, 210, 25))
        self.pushButtonNewProfile.setObjectName("pushButtonNewProfile")
        self.labelConfirmPassword = QtWidgets.QLabel(Dialog)
        self.labelConfirmPassword.setGeometry(QtCore.QRect(20, 160, 141, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelConfirmPassword.setFont(font)
        self.labelConfirmPassword.setObjectName("labelConfirmPassword")
        self.lineEditConfirmPassword = QtWidgets.QLineEdit(Dialog)
        self.lineEditConfirmPassword.setGeometry(QtCore.QRect(170, 160, 150, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEditConfirmPassword.setFont(font)
        self.lineEditConfirmPassword.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.lineEditConfirmPassword.setObjectName("lineEditConfirmPassword")
        self.pushButtonCancelProfile = QtWidgets.QPushButton(Dialog)
        self.pushButtonCancelProfile.setEnabled(False)
        self.pushButtonCancelProfile.setGeometry(QtCore.QRect(175, 200, 100, 25))
        self.pushButtonCancelProfile.setObjectName("pushButtonCancelProfile")
        self.pushButtonSubmitProfile = QtWidgets.QPushButton(Dialog)
        self.pushButtonSubmitProfile.setEnabled(False)
        self.pushButtonSubmitProfile.setGeometry(QtCore.QRect(65, 200, 100, 25))
        self.pushButtonSubmitProfile.setObjectName("pushButtonSubmitProfile")
        self.labelResponse = QtWidgets.QLabel(Dialog)
        self.labelResponse.setGeometry(QtCore.QRect(20, 260, 300, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelResponse.sizePolicy().hasHeightForWidth())
        self.labelResponse.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelResponse.setFont(font)
        self.labelResponse.setText("")
        self.labelResponse.setAlignment(QtCore.Qt.AlignCenter)
        self.labelResponse.setObjectName("labelResponse")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(48, 20, 250, 61))
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setLineWidth(1)
        self.frame.setObjectName("frame")
        self.labelTitle = QtWidgets.QLabel(self.frame)
        self.labelTitle.setGeometry(QtCore.QRect(25, 7, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.labelTitle.setFont(font)
        self.labelTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTitle.setObjectName("labelTitle")
        self.labelSubTitle = QtWidgets.QLabel(self.frame)
        self.labelSubTitle.setGeometry(QtCore.QRect(25, 32, 200, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelSubTitle.setFont(font)
        self.labelSubTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.labelSubTitle.setObjectName("labelSubTitle")
        self.frame.raise_()
        self.pushButtonSubmitProfile.raise_()
        self.pushButtonCancelProfile.raise_()
        self.labelUserProfile.raise_()
        self.labelPassword.raise_()
        self.lineEditUserProfile.raise_()
        self.lineEditPassword.raise_()
        self.pushButtonLogin.raise_()
        self.pushButtonQuit.raise_()
        self.pushButtonNewProfile.raise_()
        self.labelConfirmPassword.raise_()
        self.lineEditConfirmPassword.raise_()
        self.labelResponse.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.lineEditUserProfile, self.lineEditPassword)
        Dialog.setTabOrder(self.lineEditPassword, self.lineEditConfirmPassword)
        Dialog.setTabOrder(self.lineEditConfirmPassword, self.pushButtonLogin)
        Dialog.setTabOrder(self.pushButtonLogin, self.pushButtonQuit)
        Dialog.setTabOrder(self.pushButtonQuit, self.pushButtonNewProfile)
        Dialog.setTabOrder(self.pushButtonNewProfile, self.pushButtonSubmitProfile)
        Dialog.setTabOrder(self.pushButtonSubmitProfile, self.pushButtonCancelProfile)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Credentials"))
        self.labelUserProfile.setText(_translate("Dialog", "User Profile:"))
        self.labelPassword.setText(_translate("Dialog", "Password:"))
        self.pushButtonLogin.setText(_translate("Dialog", "Login"))
        self.pushButtonQuit.setText(_translate("Dialog", "Quit"))
        self.pushButtonNewProfile.setText(_translate("Dialog", "New Profile"))
        self.labelConfirmPassword.setText(_translate("Dialog", "Confirm Password:"))
        self.pushButtonCancelProfile.setText(_translate("Dialog", "Cancel"))
        self.pushButtonSubmitProfile.setText(_translate("Dialog", "Submit"))
        self.labelTitle.setText(_translate("Dialog", "Alchemical Finances"))
        self.labelSubTitle.setText(_translate("Dialog", "\"Hands On Personal Finance\""))

