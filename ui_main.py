import requests
import re
import smtplib
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.encoders import encode_base64
import poplib
from ui_test import Ui_MainWindow
from PyQt4 import QtGui, QtCore
import sys
import time


class EmailUser:

	def __init__(self):
		self.user = "junkuizhang@126.com"
		self.pwd = "ZJKzhangjunkui01"
		self.smtp_server = "smtp.126.com"
		self.pop_server = "pop.126.com"

	def send_captcha(self, captcha):

		def get_format_addr(data):
			name, addr = parseaddr(data)
			return formataddr((Header(name, "utf-8").encode(), addr))

		msg = MIMEMultipart()
		message = MIMEText(captcha, "plain", "utf-8")
		msg["From"] = get_format_addr("Junkui Zhang <%s>" % self.user)
		msg["To"] = get_format_addr("Me <%s>" % self.user)
		msg["Subject"] = Header("<!CAPTCHA!>", "utf-8").encode()
		msg.attach(message)

		with open("0.jpg", "rb") as file:
			pic = MIMEBase("image", "jpg", filename="0.jpg")
			pic.add_header("Content-Disposition", "attachment", filename="0.jpg")
			pic.add_header("Content-ID", "<0>")
			pic.add_header("X-Attachment-ID", "0")
			pic.set_payload(file.read())
			encode_base64(pic)
			msg.attach(pic)

		server = smtplib.SMTP(self.smtp_server, 25)
		server.login(self.user, self.pwd)
		server.sendmail(self.user, [self.user], msg.as_bytes())
		server.quit()

	def send_information(self, info, to_addr):

		def get_format_addr(data):
			name, addr = parseaddr(data)
			return formataddr((Header(name, "utf-8").encode(), addr))

		message = MIMEText(str(info), "plain", "utf-8")
		message["From"] = get_format_addr("Junkui Zhang <%s>" % self.user)
		message["To"] = get_format_addr("User <%s>" % to_addr)
		message["Subject"] = Header("这是由软件自动发出的邮件！", "utf-8").encode()

		server = smtplib.SMTP(self.smtp_server, 25)
		server.login(self.user, self.pwd)
		server.sendmail(self.user, [to_addr], message.as_string())
		server.quit()

	def read_replies(self):
		server = poplib.POP3(self.pop_server)
		server.user(self.user)
		server.pass_(self.pwd)
		# this is a placeholder


class CheckConnect(QtCore.QThread):
	sin1 = QtCore.pyqtSignal(str)

	def __init__(self, response, url, header, parent=None):
		super(CheckConnect, self).__init__(parent)
		self.url = url
		self.response = response
		self.header = header
		self.is_done = 0
		self.strings = ""
		self.res = ""

	def run(self):
		while self.is_done == 0:
			try:
				conn = self.response.get(self.url, headers=self.header)
				if re.findall('404.png', conn.text) != []:
					self.sin1.emit("连接失败，1秒后重试")
				self.res = conn
				self.is_done = 1
				self.sin1.emit("连接成功！请输入验证码！")
			except:
				self.sin1.emit("=========无法连接至验证码服务器，1秒后重试=======")


class ConnectThread(QtCore.QThread):
	sin1 = QtCore.pyqtSignal()

	def __init__(self, thread):
		super(ConnectThread, self).__init__()
		self.thread = thread

	def run(self):
		while self.thread.is_done == 0:
			self.thread.quit()
			self.thread.start()
		self.sin1.emit()


class MyWindow(QtGui.QMainWindow, Ui_MainWindow):

	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		self.setWindowTitle("自动选课器")
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("./source/logo.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.setWindowIcon(icon)
		self.login.clicked.connect(self.run)
		self.get_captcha.clicked.connect(self.get_captcha_)
		self.response = requests.session()
		self.cookie = ""
		self.auto_email = EmailUser()

	def print_info(self, string):
		self.print_window.append(string)

	def get_captcha_(self):

		def some_function():
			conn = thread1.res
			self.print_window.append("=="*20)
			self.print_window.append("成功下载验证码！请输入验证码")
			try:
				f = open("0.jpg", "wb")
				f.write(conn.content)
				f.close()
				self.captcha.setPixmap(QtGui.QPixmap("0.jpg"))
			except:
				self.print_window.append("无法打开文件")
				raise FileExistsError
			self.cookie = re.findall('kie (.*) for', str(conn.cookies))[0]

		url = "http://210.42.121.241/servlet/GenImg"
		response = requests.session()
		thread1 = CheckConnect(response, url, {})
		thread1.sin1.connect(self.print_info)
		thread2 = ConnectThread(thread1)
		thread2.sin1.connect(some_function)
		thread2.start()
		thread2.wait()

		# conn = thread1.res
		# self.print_window.append("=="*20)
		# self.print_window.append("成功下载验证码！请输入验证码")
		# try:
		# 	f = open("0.jpg", "wb")
		# 	f.write(conn.content)
		# 	f.close()
		# 	self.captcha.setPixmap(QtGui.QPixmap("0.jpg"))
		# except:
		# 	self.print_window.append("无法打开文件")
		# 	raise FileExistsError
		# self.cookie = re.findall('kie (.*) for', str(conn.cookies))[0]

	def get_course(self):
		courses = list()
		courses.append(self.course_1.toPlainText())
		courses.append(self.course_2.toPlainText())
		courses.append(self.course_3.toPlainText())
		courses.append(self.course_4.toPlainText())
		courses.append(self.course_5.toPlainText())
		courses.append(self.course_6.toPlainText())
		return courses

	def run(self):
		url = "http://210.42.121.241/servlet/Login"
		self.print_window.append("正在登录...")
		captcha = self.captcha_2.toPlainText()
		response = self.response
		cookie = self.cookie
		username = self.user_name.toPlainText()
		password = self.password.toPlainText()
		headers = {
			"Cookie": cookie,
		}
		post_data = {
			"id": username,
			"pwd": password,
			"xdvfb": captcha
		}
		while True:
			try:
				response = response.post(url, headers=headers, data=post_data)
				if re.findall("用户名/密码错误", response.text) != []:
					self.print_window.append("用户名/密码错误")
					continue
				elif re.findall('验证码错误', response.text) != []:
					self.print_window.append("验证码错误")
					continue
				elif re.findall("404.png", response.text) != []:
					self.print_window.append("登录服务器超时")
					continue
				self.auto_email.send_captcha(captcha)
				break
			except:
				self.print_window.append("登陆失败，1秒后重试")
				continue
		self.print_window.append("=="*20)
		self.print_window.append("登录成功")
		courses = self.get_course()
		self.print_window.append("正在提交课程...")
		post_data = []
		for cou in courses:
			post_data.append(("apply", cou))
		headers = {
			"Cookie": cookie
		}
		while True:
			try:
				conn = self.response.post(url,headers=headers, data=post_data)
				if re.findall('恭喜您，申请单提交成功！', conn.text) != []:
					self.print_window.append("提交失败，自动重试...")
					break
				else:
					raise ConnectionError
			except:
				self.print_window.append("提交失败")
				continue


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	w = MyWindow()
	w.setWindowTitle("Hello")
	w.show()
	sys.exit(app.exec_())
	# s.main()