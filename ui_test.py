# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_test.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(733, 546)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.user_name = QtGui.QTextEdit(self.centralwidget)
        self.user_name.setGeometry(QtCore.QRect(110, 50, 211, 31))
        self.user_name.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.user_name.setObjectName(_fromUtf8("user_name"))
        self.tips_user_name = QtGui.QLabel(self.centralwidget)
        self.tips_user_name.setGeometry(QtCore.QRect(10, 50, 101, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(16)
        self.tips_user_name.setFont(font)
        self.tips_user_name.setObjectName(_fromUtf8("tips_user_name"))
        self.tips_password = QtGui.QLabel(self.centralwidget)
        self.tips_password.setGeometry(QtCore.QRect(10, 90, 101, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(16)
        self.tips_password.setFont(font)
        self.tips_password.setObjectName(_fromUtf8("tips_password"))
        self.password = QtGui.QTextEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(110, 90, 211, 31))
        self.password.setObjectName(_fromUtf8("password"))
        self.captcha = QtGui.QLabel(self.centralwidget)
        self.captcha.setGeometry(QtCore.QRect(170, 140, 131, 31))
        self.captcha.setText(_fromUtf8(""))
        self.captcha.setPixmap(QtGui.QPixmap(_fromUtf8("0.jpg")))
        self.captcha.setObjectName(_fromUtf8("captcha"))
        self.captcha_2 = QtGui.QTextEdit(self.centralwidget)
        self.captcha_2.setGeometry(QtCore.QRect(110, 180, 211, 31))
        self.captcha_2.setObjectName(_fromUtf8("captcha_2"))
        self.tips_captcha_2 = QtGui.QLabel(self.centralwidget)
        self.tips_captcha_2.setGeometry(QtCore.QRect(20, 180, 81, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("宋体"))
        font.setPointSize(16)
        self.tips_captcha_2.setFont(font)
        self.tips_captcha_2.setObjectName(_fromUtf8("tips_captcha_2"))
        self.login = QtGui.QPushButton(self.centralwidget)
        self.login.setGeometry(QtCore.QRect(130, 240, 121, 51))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("黑体"))
        font.setPointSize(16)
        self.login.setFont(font)
        self.login.setObjectName(_fromUtf8("login"))
        self.print_window = QtGui.QTextBrowser(self.centralwidget)
        self.print_window.setGeometry(QtCore.QRect(10, 320, 711, 181))
        self.print_window.setObjectName(_fromUtf8("print_window"))
        self.course_1 = QtGui.QTextEdit(self.centralwidget)
        self.course_1.setGeometry(QtCore.QRect(360, 10, 361, 41))
        self.course_1.setObjectName(_fromUtf8("course_1"))
        self.course_2 = QtGui.QTextEdit(self.centralwidget)
        self.course_2.setGeometry(QtCore.QRect(357, 60, 361, 41))
        self.course_2.setObjectName(_fromUtf8("course_2"))
        self.course_3 = QtGui.QTextEdit(self.centralwidget)
        self.course_3.setGeometry(QtCore.QRect(357, 110, 361, 41))
        self.course_3.setObjectName(_fromUtf8("course_3"))
        self.course_4 = QtGui.QTextEdit(self.centralwidget)
        self.course_4.setGeometry(QtCore.QRect(357, 160, 361, 41))
        self.course_4.setObjectName(_fromUtf8("course_4"))
        self.course_5 = QtGui.QTextEdit(self.centralwidget)
        self.course_5.setGeometry(QtCore.QRect(357, 210, 361, 41))
        self.course_5.setObjectName(_fromUtf8("course_5"))
        self.course_6 = QtGui.QTextEdit(self.centralwidget)
        self.course_6.setGeometry(QtCore.QRect(357, 260, 361, 41))
        self.course_6.setObjectName(_fromUtf8("course_6"))
        self.get_captcha = QtGui.QPushButton(self.centralwidget)
        self.get_captcha.setGeometry(QtCore.QRect(10, 130, 131, 41))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("黑体"))
        font.setPointSize(12)
        self.get_captcha.setFont(font)
        self.get_captcha.setObjectName(_fromUtf8("get_captcha"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 733, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.user_name.setToolTip(_translate("MainWindow", "<html><head/><body><p>在这里输入你的学号</p></body></html>", None))
        self.tips_user_name.setText(_translate("MainWindow", "你的学号", None))
        self.tips_password.setText(_translate("MainWindow", "你的密码", None))
        self.password.setToolTip(_translate("MainWindow", "<html><head/><body><p>在这里输入你的密码</p></body></html>", None))
        self.captcha.setToolTip(_translate("MainWindow", "<html><head/><body><p>验证码</p></body></html>", None))
        self.captcha_2.setToolTip(_translate("MainWindow", "<html><head/><body><p>在这里输入上图的验证码</p></body></html>", None))
        self.tips_captcha_2.setText(_translate("MainWindow", "验证码:", None))
        self.login.setToolTip(_translate("MainWindow", "<html><head/><body><p>登录</p></body></html>", None))
        self.login.setText(_translate("MainWindow", "登录", None))
        self.get_captcha.setText(_translate("MainWindow", "获取验证码", None))

