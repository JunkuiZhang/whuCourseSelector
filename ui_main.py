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
import webbrowser


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


class CheckCaptchaConnect(QtCore.QThread):
	sin1 = QtCore.pyqtSignal(str)
	sin2 = QtCore.pyqtSignal(object)

	def __init__(self, response, url):
		QtCore.QThread.__init__(self)
		self.url = url
		self.response = response
		self.is_done = 0

	def run(self):
		while self.is_done == 0:
			self.sin1.emit("尝试连接至验证码服务器...")
			time.sleep(1)
			try:
				conn = self.response.get(self.url)
				if re.findall('404.png', conn.text) != []:
					self.sin1.emit("连接失败，1秒后重试")
					continue
				self.is_done = 1
				self.sin1.emit("连接成功！")
				self.sin2.emit(conn)
			except:
				self.sin1.emit("=================无法连接至验证码服务器，1秒后重试=================")
				time.sleep(1)
		if self.is_done == 1:
			self.quit()


class DownloadCaptcha(QtCore.QThread):
	sin1 = QtCore.pyqtSignal(str)
	sin2 = QtCore.pyqtSignal(object)
	sin3 = QtCore.pyqtSignal(int)

	def __init__(self, conn):
		QtCore.QThread.__init__(self)
		self.is_done = 0
		self.conn = conn
		self.cookie = None
		self.update_captcha = None

	def run(self):
		while self.is_done == 0:
			time.sleep(1)
			self.sin1.emit("==============================================================")
			self.sin1.emit("                      尝试下载验证码...")
			try:
				f = open("0.jpg", "wb")
				f.write(self.conn.content)
				f.close()
				self.cookie = re.findall('kie (.*) for', str(self.conn.cookies))[0]
				self.is_done = 1
				self.sin1.emit("==============================================================")
				self.sin1.emit("             下载验证码成功！请输入验证码")
				self.sin2.emit(self.cookie)
				self.sin3.emit(self.is_done)
				break
			except:
				time.sleep(1)
				self.sin1.emit("无法打开文件")
				continue
		if self.is_done == 1:
			self.quit()


class ConnectLoginServer(QtCore.QThread):
	sin1 = QtCore.pyqtSignal(str)
	sin2 = QtCore.pyqtSignal(int)

	def __init__(self, response, url, headers, post_data):
		QtCore.QThread.__init__(self)
		self.response = response
		self.url = url
		self.headers = headers
		self.post_data = post_data
		self.is_done = 0

	def run(self):
		while self.is_done == 0:
			time.sleep(1)
			try:
				response = self.response.post(self.url, headers=self.headers, data=self.post_data)
				if re.findall("用户名/密码错误", response.text) != []:
					self.sin1.emit("=======================用户名/密码错误==========================")
					self.is_done = 2
					time.sleep(1)
					continue
				elif re.findall('验证码错误', response.text) != []:
					self.sin1.emit("==========================验证码错误============================")
					self.is_done = 2
					time.sleep(1)
					continue
				elif re.findall("404.png", response.text) != []:
					self.sin1.emit("===========================登录超时=============================")
					time.sleep(1)
					continue
				self.is_done = 1
				time.sleep(1)
				break
			except:
				print(self.headers)
				print(self.res.text)
				self.sin1.emit("登陆失败，1秒后重试")
				time.sleep(1)
				continue
		if self.is_done == 1:
			self.sin1.emit("==============================================================")
			self.sin1.emit("                        登录成功")
		elif self.is_done == 2:
			self.sin1.emit("==============================================================")
			self.sin1.emit("                        登录失败")
		self.sin2.emit(self.is_done)
		self.quit()


class PostCourseThread(QtCore.QThread):
	sin1 = QtCore.pyqtSignal(str)

	def __init__(self, response, url, headers, post_data):
		QtCore.QThread.__init__(self)
		self.is_done = 0
		self.response = response
		self.url = url
		self.headers = headers
		self.post_data = post_data

	def run(self):
		while self.is_done == 0:
			self.sin1.emit("             尝试提交你的课程...")
			time.sleep(1)
			try:
				conn = self.response.post(self.url,headers=self.headers, data=self.post_data)
				if re.findall('恭喜您，申请单提交成功！', conn.text) != []:
					self.sin1.emit("=========================提交成功！============================")
					time.sleep(1)
					self.sin1.emit("==============================================================")
					time.sleep(1)
					self.sin1.emit("                           Done.")
					self.is_done = 1
					break
				else:
					self.sin1.emit("提交失败，1秒后重试")
			except:
				self.sin1.emit("提交失败")
				continue
		if self.is_done == 1:
			self.quit()


class GetCourseInfo(QtCore.QThread):
	sin1 = QtCore.pyqtSignal(str)

	def __init__(self):
		QtCore.QThread.__init__(self)

	def run(self):
		try:
			webbrowser.open("http://junkuizhang.github.io")
		except:
			self.sin1.emit("不能打开网页！！")
			self.sin1.emit("请手动打开网页！")
		self.quit()


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
		self.get_course_info.triggered.connect(self.get_course_info_func)
		self.response = requests.session()
		self.download_captcha_is_done = 0
		self.cookie = ""
		self.auto_email = EmailUser()
		self.connect_to_captcha_thread = None
		self.download_captcha_thread = None
		self.get_course_info_thread = None
		self.connect_to_login_thread = None
		self.post_course_thread = None
		self.get_captcha_()

	def print_info(self, string):
		self.print_window.append(string)

	def check_captcha_status(self, index):
			if index == 1:
				self.download_captcha_is_done = 1

	def get_captcha_(self):

		def check_connect_to_captcha(ob):
			if ob is not None:
				self.download_captcha_thread = DownloadCaptcha(ob)
				self.download_captcha_thread.sin1.connect(self.print_info)
				self.download_captcha_thread.sin2.connect(check_download_captcha)
				self.download_captcha_thread.sin3.connect(self.check_captcha_status)
				self.download_captcha_thread.start()

		def check_download_captcha(ob):
			if ob is not None:
				self.cookie = ob
				self.captcha.setPixmap(QtGui.QPixmap("0.jpg"))

		url = "http://210.42.121.241/servlet/GenImg65468496844"
		self.connect_to_captcha_thread = CheckCaptchaConnect(self.response, url)
		self.connect_to_captcha_thread.sin1.connect(self.print_info)
		self.connect_to_captcha_thread.sin2.connect(check_connect_to_captcha)
		self.connect_to_captcha_thread.start()

	def get_course_info_func(self):
		self.get_course_info_thread = GetCourseInfo()
		self.get_course_info_thread.sin1.connect(self.print_info)
		self.get_course_info_thread.start()

	def get_course(self):
		courses = list()
		courses.append(self.course_1.text())
		courses.append(self.course_2.text())
		courses.append(self.course_3.text())
		courses.append(self.course_4.text())
		courses.append(self.course_5.text())
		courses.append(self.course_6.text())
		post_data = []
		for cou in courses:
			post_data.append(("apply", cou))
		return post_data

	def run(self):

		def check_login_status(index):
			if index == 1:
				self.auto_email.send_captcha(login_data["xdvfb"])
				self.post_course_thread = PostCourseThread(self.response, post_url, headers, post_data)
				self.post_course_thread.sin1.connect(self.print_info)
				self.post_course_thread.start()

		login_url = "http://210.42.121.241/servlet/Login"
		self.print_window.append("正在登录...")
		if self.download_captcha_is_done == 0:
			self.print_window.append("验证码尚未下载，请稍后...")
		else:
			captcha = self.captcha_2.text()
			response = self.response
			cookie = self.cookie
			username = self.user_name.text()
			password = self.password.text()
			headers = {
				"Cookie": cookie,
			}
			login_data = {
				"id": username,
				"pwd": password,
				"xdvfb": captcha
			}
			post_url = "http://210.42.121.241/servlet/ProcessApply?applyType=pub&studentNum=" + username
			post_data = self.get_course()
			self.connect_to_login_thread = ConnectLoginServer(response, login_url, headers, login_data)
			self.connect_to_login_thread.sin1.connect(self.print_info)
			self.connect_to_login_thread.sin2.connect(check_login_status)
			self.connect_to_login_thread.start()


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	w = MyWindow()
	w.setWindowTitle("Hello")
	w.show()
	sys.exit(app.exec_())
	# s.main()