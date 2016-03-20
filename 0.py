import requests
import re
from ui_test import Ui_MainWindow
from PyQt4 import QtGui, QtCore
import sys


class ConnectThread(QtCore.QThread):
	sin1 = QtCore.pyqtSignal(str)

	def __init__(self, response, url):
		QtCore.QThread.__init__(self)
		self.response = response
		self.url = url

	def run(self):
		try:
			self.sin1.emit("???")
			self.response.get(self.url)
			self.sin1.emit("Yes")
		except:
			self.sin1.emit("No")


class MyWindow(QtGui.QMainWindow, Ui_MainWindow):

	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		self.setWindowTitle("自动选课器")
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("./source/logo.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.setWindowIcon(icon)
		self.get_captcha.clicked.connect(self.connect_to_captcha)
		self.response = requests.session()

	def print_something(self, string):
		print(string)

	def connect_to_captcha(self):
		url = "https://www.google.com"
		thread = ConnectThread(self.response, url)
		thread.sin1.connect(self.print_something)
		thread.moveToThread(self.response, url)


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	w = MyWindow()
	w.setWindowTitle("Hello")
	w.show()
	sys.exit(app.exec_())
	# s.main()
