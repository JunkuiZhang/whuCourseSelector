import requests
import re
from ui_test import Ui_MainWindow
from PyQt4 import QtGui, QtCore
import sys
import threading


class ConnectThread(QtCore.QThread):
	sin1 = QtCore.pyqtSignal(str)

	def __init__(self, response, url):
		# threading.Thread.__init__(self)
		QtCore.QThread.__init__(self)
		self.response = response
		self.url = url
		self.strings = "gdfgd"

	def run(self):
		while True:
			self.sin1.emit("Trying")
			try:
				self.response.get(self.url)
				self.sin1.emit("Hello")
				break
			except:
				self.sin1.emit("No")
				continue


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

	def update_text(self, string):
		self.print_window.append(string)

	def connect_to_captcha(self):
		url = "http://210.42.121.241/servlet/GenImg"
		url = "www.google.com"
		# thread = ConnectToServer(self.response, url)
		# thread.start()
		# print(thread.strings)
		thread = ConnectThread(self.response, url)
		thread.sin1.connect(self.update_text)
		thread.start()
		# th = LoopConnect(thread)
		# th.sin1.connect(self.let_do_something)
		# th.start()
		thread.wait()
		# th.wait()


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	w = MyWindow()
	w.setWindowTitle("Hello")
	w.show()
	sys.exit(app.exec_())
	# s.main()
