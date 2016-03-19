import requests
import re
import bs4
import csv

class Course:

	def __init__(self, user="2013301000021", pwd="zjk1995"):
		self.user = user
		self.pwd = pwd

	def connectServer(self, url, response, headers):
		try:
			res = response.get(url, headers=headers)
		except:
			print("Cant connect to the server.")
			raise ConnectionError
		if re.findall("游客登录", res.text) != []:
			print("="*6 + "Invalid captcha or information." + "="*6)
			raise ValueError
		elif re.findall("404.png", res.text) != []:
			print("="*6 + "Server error." + "="*6)
			raise ValueError
		else:
			return {"res": res, "session": response}

	def connectServerPost(self, url, response, headers, data):
		try:
			res = response.post(url, headers=headers, data=data)
		except:
			print("Cant connect to the server.")
			raise ConnectionError
		if re.findall("游客登录", res.text) != []:
			print("="*6 + "Invalid captcha or information." + "="*6)
			raise ValueError
		elif re.findall("404.png", res.text) != []:
			print("="*6 + "Post server error." + "="*6)
			raise ConnectionError
		else:
			return response

	def getCaptha(self):
		url = "http://210.42.121.241/servlet/GenImg"
		response = requests.session()
		conn = self.connectServer(url, response, headers={})
		res = conn["res"]
		try:
			f = open("0.jpg", "wb")
			f.write(res.content)
			f.close()
		except ValueError("Can't write the captcha picture."):
			raise
		captcha = input("Enter the strings: ")
		cookie = res.cookies
		cookie = re.findall('kie (.*) for', str(cookie))[0]
		return {"captcha": captcha, "session": conn["session"], "cookie": cookie}

	def checkUser(self, response, cookie, captcha):
		headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
			"Cookie": cookie
		}
		login_url = "http://210.42.121.241/servlet/Login"
		post_data = {
			"id": self.user,
			"pwd": self.pwd,
			"xdvfb": captcha
		}
		response = self.connectServerPost(login_url, response, headers=headers, data=post_data)
		list_url = "http://210.42.121.241/stu/choose_PubLsn_list.jsp?XiaoQu=0&credit=0&keyword=&pageNum=1"
		conn = self.connectServer(list_url, response=response, headers=headers)
		return conn

	def main(self, ls):
		captcha = ls["captcha"]
		response = ls["session"]
		cookie = ls["cookie"]
		res = self.checkUser(response, cookie, captcha)
		soup = bs4.BeautifulSoup(res["res"].text, "html.parser")
		pagenum = soup.find_all("div")[-1]
		pagenum = re.findall('记录 第1/([0-9]+)页', str(pagenum))[0]
		try:
			f = open("course_info.csv", "w", newline="")
			w = csv.writer(f)
			w.writerow(["CourseName", "Credit", "Class", "CourseID"])
		except ValueError("Cant write information in file!"):
			raise
		headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
			"Cookie": cookie
		}
		response = res["session"]
		for i in range(int(pagenum)):
			list_url = "http://210.42.121.241/stu/choose_PubLsn_list.jsp?XiaoQu=0&credit=0&keyword=&pageNum=" + str(i + 1)
			res2 = self.connectServer(list_url, response=response, headers=headers)
			soup = bs4.BeautifulSoup(res2["res"].text, "html.parser")
			course = soup.find_all("tr")
			course.pop(0)
			for c in course:
				s = bs4.BeautifulSoup(str(c), "html.parser")
				info = s.find_all("td")
				print("=="*30)
				name = re.findall('<td>(.*)<', str(info[0]))[0]
				credit = re.findall('<td>(.*)<', str(info[1]))[0]
				_class = str(s.find_all("div")[-1].string).strip()
				ids = info[-1]
				c_id = re.findall('" id="([0-9]+)" ', str(ids))[0]
				print(name)
				print(credit)
				print(_class)
				print(c_id)
				w.writerow([name, credit, _class, c_id])
				print("Done.")
		f.close()

if __name__ == "__main__":
	c = Course()
	ls = c.getCaptha()
	c.main(ls)