import urllib.request
import re
import random
def getdata(url,page):
	header = ("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")
	#headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
	proxyadd = random.choice(["189.208.39.201:3128","89.36.213.173:1189","117.143.109.163:80","117.143.109.143:80"])
	proxy = urllib.request.ProxyHandler({'http':proxyadd})
	opener = urllib.request.build_opener(proxy)
	opener.add_handlers = [header]
	urllib.request.install_opener(opener)
	data = urllib.request.urlopen(url).read().decode('gbk')
	userpat = 'target="_blank" title="(.*?)">'
	content_pat = '<div class="content">(.*?)</div>'
	userlist =re.compile(userpat,re.S).findall(data)
	content_list = re.compile(content_pat,re.S).findall(data)
	x = 1
	for content in content_list:
		content = content.replace("\n",'')
		name = "content"+str(x)
		exec(name+'=content')
		x+=1
	y = 1
	for user in userlist:
		name = "content"+str(y)
		print("用户"+str(page)+str(y)+"是："+user)
		print("内容是：")
		exec ("print("+name+")")
		print("\n")
		y+=1
for i in range(1,40):
	url = "https://www.qiushibaike.com/"
	getdata(url,i)