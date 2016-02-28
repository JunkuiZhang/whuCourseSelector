import bs4
import re

f = open("0.txt", "r")
data = f.read()
f.close()

soup = bs4.BeautifulSoup(data)
course = soup.find_all("tr")
course.pop(0)
for c in course:
	print("=="*30)
	soup = bs4.BeautifulSoup(str(c), "html.parser")
	info = soup.find_all("td")
	name = re.findall('<td>(.*)<', str(info[0]))[0]
	credit = re.findall('<td>(.*)<', str(info[1]))[0]
	c = soup.find_all("div")[-1].string
	print(name)
	print(credit)
	print(str(c).strip())