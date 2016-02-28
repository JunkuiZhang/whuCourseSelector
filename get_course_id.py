import requests
import re
import bs4
import csv

class Course:

	def __init__(self, user="2013301000021", pwd="zjk1995"):
		self.user = user
		self.pwd = pwd

	def getCaptha(self):
		url = "http://210.42.121.241/servlet/GenImg"
		response = requests.session()
		res = response.get(url)
		f = open("0.jpg", "wb")
		f.write(res.content)
		f.close()
		captcha = input("Enter the strings: ")
		cookie = res.cookies
		cookie = re.findall('kie (.*) for', str(cookie))[0]
		return [captcha, response, cookie]

	def main(self, ls):
		captcha = ls[0]
		response = ls[1]
		cookie = ls[2]
		login_url = "http://210.42.121.241/servlet/Login"
		headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
			"Cookie": cookie
		}
		post_data = {
			"id": self.user,
			"pwd": self.pwd,
			"xdvfb": captcha
		}
		res0 = response.post(login_url, headers=headers, data=post_data)
		list_url = "http://210.42.121.241/stu/choose_PubLsn_list.jsp?XiaoQu=0&credit=0&keyword=&pageNum=1"
		res1 = response.get(list_url, headers=headers)
		soup = bs4.BeautifulSoup(res1.text, "html.parser")
		pagenum = soup.find_all("div")[-1]
		pagenum = re.findall('记录 第1/([0-9]+)页', str(pagenum))[0]
		f = open("course_info.csv", "w")
		w = csv.writer(f)
		w.writerow(["CourseName", "Credit", "Class"])
		for i in range(int(pagenum)):
			list_url = "http://210.42.121.241/stu/choose_PubLsn_list.jsp?XiaoQu=0&credit=0&keyword=&pageNum=" + str(i + 1)
			res2 = response.get(list_url, headers=headers)
			soup = bs4.BeautifulSoup(res2.text, "html.parser")
			course = soup.find_all("tr")
			course.pop(0)
			for c in course:
				s = bs4.BeautifulSoup(str(c), "html.parser")
				info = s.find_all("td")
				print("=="*30)
				name = re.findall('<td>(.*)<', str(info[0]))[0]
				credit = re.findall('<td>(.*)<', str(info[1]))[0]
				_class = str(s.find_all("div")[-1].string).strip()
				print(name)
				print(credit)
				print(_class)
				w.writerow([name, credit, _class])
				print("Done.")
		f.close()

c = Course()
ls = c.getCaptha()
c.main(ls)