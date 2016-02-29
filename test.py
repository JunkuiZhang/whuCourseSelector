import bs4
import re

f = open("0.txt", "r")
data = f.read()
f.close()

soup = bs4.BeautifulSoup(data, "html.parser")
course = soup.find_all("tr")
course.pop(0)
for c in course:
	print("=="*30)
	soup = bs4.BeautifulSoup(str(c), "html.parser")
	infos = soup.find_all("td")
	info = infos
	ids = infos[-1]
	name = re.findall('<td>(.*)<', str(info[0]))[0]
	credit = re.findall('<td>(.*)<', str(info[1]))[0]
	c = soup.find_all("div")[-1].string
	c_id = re.findall('" id="([0-9]+)" ', str(ids))[0]
	print(name)
	print(credit)
	print(str(c).strip())
	print(c_id)