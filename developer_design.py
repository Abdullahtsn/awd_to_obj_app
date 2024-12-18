# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'developer_design.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(437, 142)
        Form.setStyleSheet("QPushButton{\n"
"\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background-color: rgb(138, 0, 0);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: rgb(255, 252, 237);\n"
"}\n"
"\n"
"\n"
"QLabel{\n"
"font: 75 16pt \"MS Shell Dlg 2\";\n"
"    color: rgb(211, 225, 255);\n"
"}\n"
"QWidget{\n"
"    background-color: rgb(0, 0, 0);\n"
"}\n"
"")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(25, 5, 5, 10)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_communication = QtWidgets.QLabel(Form)
        self.label_communication.setStyleSheet("color: rgb(75, 151, 227);\n"
"font: 87 12pt \"Arial Black\";")
        self.label_communication.setObjectName("label_communication")
        self.verticalLayout.addWidget(self.label_communication, 0, QtCore.Qt.AlignHCenter)
        self.label_github = QtWidgets.QLabel(Form)
        self.label_github.setObjectName("label_github")
        self.verticalLayout.addWidget(self.label_github)
        self.label_gmail = QtWidgets.QLabel(Form)
        self.label_gmail.setObjectName("label_gmail")
        self.verticalLayout.addWidget(self.label_gmail)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_close = QtWidgets.QPushButton(Form)
        self.pushButton_close.setText("")
        self.pushButton_close.setObjectName("pushButton_close")
        self.verticalLayout_2.addWidget(self.pushButton_close)
        self.pushButton_github = QtWidgets.QPushButton(Form)
        self.pushButton_github.setText("")
        self.pushButton_github.setObjectName("pushButton_github")
        self.verticalLayout_2.addWidget(self.pushButton_github)
        self.pushButton_gmail = QtWidgets.QPushButton(Form)
        self.pushButton_gmail.setText("")
        self.pushButton_gmail.setObjectName("pushButton_gmail")
        self.verticalLayout_2.addWidget(self.pushButton_gmail)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_communication.setText(_translate("Form", "COMMUNICATION"))
        self.label_github.setText(_translate("Form", "https://github.com/Abdullahtsn"))
        self.label_gmail.setText(_translate("Form", "abdullah.tosun.9696@gmail.com"))
