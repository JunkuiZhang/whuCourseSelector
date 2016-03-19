import requests
import re

captcha_url = "http://210.42.121.241/servlet/GenImg"
captcha_info = requests.get(captcha_url)
cookie = re.findall('kie (.*) for', str(captcha_info.cookies))[0]
f = open("0.jpg", "wb")
f.write(captcha_info.content)
f.close()

captcha = input("Strings in the pic: ")
post_url = "http://210.42.121.241/servlet/Login"
headers = {
	"Cookie": cookie
}
post_data = {
	"id": "2013301000021",
	"pwd": "zjk1995",
	"xdvfb": captcha
}
res = requests.post(post_url, headers=headers, data=post_data)

list_url = "http://210.42.121.241/stu/choose_PubLsn_list.jsp?XiaoQu=0&credit=0&keyword=&pageNum=1"
res1 = requests.get(list_url, headers=headers)

print(res.text)
print("="*20)
print(res.reason)
print("="*20)
if re.findall('用户名/密码错误', str(res.text)) != []:
	print("User id or pwd incorrect.")
else:
	print("User id and pwd are correct.")

if re.findall('游客登录只需输入验证码', str(res1.text)) != []:
	print("Failed to login.")
else:
	print("Login successful")