import requests
import re

class Selector:

	def __init__(self, user, pwd):
		self.username = user
		self.password = pwd

	def getCaptha(self):
		url = "http://210.42.121.241/servlet/GenImg"
		response = requests.session()
		res = response.get(url)
		f = open("0.jpg", "wb")
		f.write(res.content)
		f.close()
		self.cookie = re.findall('kie (.*) for', str(res.cookies))[0]
		cap = input("Plz enter the strings in the pic: ")
		return {"cap": cap, "response": response}

	def checkUser(self):
		url = "http://210.42.121.241/servlet/Login"
		keys = self.getCaptha()
		captcha = keys["cap"]
		response = keys["response"]
		headers = {
			"Cookie": self.cookie,
			"Host": "210.42.121.241",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
			"Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
			"Accept-Encoding": "gzip, deflate",
			"Referer": "http://210.42.121.241/",
			"Connection": "keep-alive"
		}
		post_data = {
			"id": self.username,
			"pwd": self.password,
			"xdvfb": captcha
		}
		res = response.post(url, data=post_data, headers=headers)
		res = response.get("http://210.42.121.241/stu/stu_index.jsp", headers=headers)
		if re.findall("验证码错误", str(res.text)) != []:
			print("Failed to login, wrong captcha.")
			raise ValueError
		elif re.findall("用户名/密码错误", str(res.text)) != []:
			print("Failed to login, wrong user name or password.")
			raise ValueError
		elif re.findall("游客登录", str(res.text)) != []:
			print("Failed to login.")
			raise ValueError
		print("=="*30)
		print("Login successfully")
		print("=="*30)
		return response

	def getCourse(self):
		cour = list()
		num = 0
		for i in range(6):
			print("Enter 'finish' to finish.")
			print("Selected %s courses." % str(i))
			course = input("Enter your %s course id:" % str(i + 1))
			if course == "finish":
				break
			cour.append(course)
			num = i + 1
		return [cour, num]

	def main(self):
		url = "http://210.42.121.241/servlet/ProcessApply?applyType=pub&studentNum=" + self.username
		response = self.checkUser()
		ls = self.getCourse()
		course = ls[0]
		num = ls[1]
		print(" ")
		print("Posting your courses...")
		if num == 1:
			post_data = {"apply": course[0]}
		elif num == 2:
			post_data = [("apply", course[0]), ("apply", course[1])]
		elif num == 3:
			post_data = [("aplly", course[0]), ("apply", course[1]), ("apply", course[2])]
		elif num == 4:
			post_data = [("aplly", course[0]), ("apply", course[1]), ("apply", course[2]), ("apply", course[3])]
		elif num == 5:
			post_data = [("aplly", course[0]), ("apply", course[1]), ("apply", course[2]), ("apply", course[3]), ("apply", course[4])]
		else:
			post_data = [("aplly", course[0]), ("apply", course[1]), ("apply", course[2]), ("apply", course[3]), ("apply", course[4]), ("qpply", course[5])]
		headers={
			"Host": "210.42.121.241",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
			"Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
			"Accept-Encoding": "gzip, deflate",
			"Referer": "http://210.42.121.241/stu/choose_Publsn_Apply.jsp",
			"Connection": "keep-alive",
			"Cookie": self.cookie
		}
		res = response.post(url, data=post_data, headers=headers)
		info = re.findall('恭喜您，申请单提交成功！', res.text)
		if info != []:
			print("=="*30)
			print("Done")
			print("Selected courses:")
			for n in course:
				print(n)
		else:
			print("Error")


s = Selector("2013301000021", "zjk1995")
s.main()