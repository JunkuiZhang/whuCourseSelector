import requests
import re


class Selector:

	def __init__(self, user, pwd):
		self.username = user
		self.password = pwd

	def connectServer(self, url, response, headers):
		try:
			res = response.get(url, headers=headers)
		except:
			print("Cant connect to the target server.")
			raise ConnectionError
		if re.findall("游客登录", res.text) != []:
			print("="*6 + "Invalid captcha or information." + "="*6)
			raise ValueError
		elif re.findall("404.png", res.text) != []:
			print("="*6 + "Server error." + "="*6)
			raise ConnectionError
		else:
			return {"res": res, "session": response}

	def connectServerPost(self, url, response, headers, data):
		try:
			res = response.post(url, headers=headers, data=data)
		except:
			print("Cant connect to the post server.")
			raise ConnectionError
		if re.findall("游客登录", res.text) != []:
			print("="*6 + "Invalid captcha or information." + "="*6)
			raise ValueError
		elif re.findall("404.png", res.text) != []:
			print("="*6 + "Post server error." + "="*6)
			raise ConnectionError
		else:
			return {"res": res, "session": response}

	def getCaptha(self):
		url = "http://210.42.121.241/servlet/GenImg"
		response = requests.session()
		conn = self.connectServer(url, response=response, headers={})
		res = conn["res"]
		response = conn["session"]
		try:
			f = open("0.jpg", "wb")
			f.write(res.content)
			f.close()
		except:
			print("Cant open jpg file.")
			raise FileExistsError
		cookie = re.findall('kie (.*) for', str(res.cookies))[0]
		cap = input("Plz enter the strings in the pic: ")
		return {"cap": cap, "response": response, "cookie": cookie}

	def checkUser(self):
		url = "http://210.42.121.241/servlet/Login"
		keys = self.getCaptha()
		captcha = keys["cap"]
		response = keys["response"]
		cookie = keys["cookie"]
		headers = {
			"Cookie": cookie,
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
		}
		post_data = {
			"id": self.username,
			"pwd": self.password,
			"xdvfb": captcha
		}
		response = self.connectServerPost(url, response=response, headers=headers, data=post_data)["session"]
		conn = self.connectServer("http://210.42.121.241/stu/stu_index.jsp", response=response, headers=headers)
		response = conn["session"]
		print("=="*30)
		print("Login successfully")
		print("=="*30)
		return {"session": response, "cookie": cookie}

	def getCourse(self):
		cour = list()
		for i in range(6):
			print("Enter 'finish' to finish.")
			print("Selected %s courses." % str(i))
			course = input("Enter your %s course id:" % str(i + 1))
			if course == "finish":
				break
			cour.append(course)
		return cour

	def main(self):
		url = "http://210.42.121.241/servlet/ProcessApply?applyType=pub&studentNum=" + self.username
		infos = self.checkUser()
		course = self.getCourse()
		response = infos["session"]
		cookie = infos["cookie"]
		print(" ")
		print("Posting your courses...")
		post_data = []
		for cou in course:
			post_data.append(("apply", cou))
		headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
			"Cookie": cookie
		}
		conn = self.connectServerPost(url, response=response, headers=headers, data=post_data)
		res = conn["res"]
		info = re.findall('恭喜您，申请单提交成功！', res.text)
		if info != []:
			print("=="*30)
			print("Done")
			print("Selected courses:")
			for n in course:
				print(n)
		else:
			print("Error")


if __name__ == "__main__":
	s = Selector("2013301000021", "zjk1995")
	s.main()