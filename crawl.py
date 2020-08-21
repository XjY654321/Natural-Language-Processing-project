# this file is used to crawl data from websites
import re, requests
from bs4 import BeautifulSoup
import os
import time,random

#craw url list
crawlist = []

strhtml = requests.Session().get('https://www.theguardian.com/environment/climate-change')
soup = BeautifulSoup(strhtml.text,'lxml')
rtn = soup.find('script', {'data-schema':'ItemList'})
for rt in rtn:
	# print(rt.strip())
	dic = eval(rt.strip())
	# print(dic.keys())
	# print(dic["itemListElement"])
	for u in dic["itemListElement"]:
		print(u['url'])
		crawlist.append(u['url'])

rtnext = soup.find('link', {'rel':'next'})
while rtnext is not None and len(crawlist)<1000: #1000 6M
	print(rtnext['href'])
	url = rtnext['href']
	strhtml = requests.Session().get(url)
	soup = BeautifulSoup(strhtml.text,'lxml')
	rtn = soup.find('script', {'data-schema':'ItemList'})
	for rt in rtn:
		dic = eval(rt.strip())
		# print(dic.keys())
		# print(dic["itemListElement"])
		for u in dic["itemListElement"]:
			print(u['url'])
			crawlist.append(u['url'])
	rtnext = soup.find('link', {'rel':'next'})

urls = [
'https://www.theguardian.com/sport/golf',
'https://www.theguardian.com/sport/formulaone',
'https://www.theguardian.com/sport/cycling',
'https://www.theguardian.com/sport/tennis',
'https://www.theguardian.com/sport/rugby-union',
'https://www.theguardian.com/sport/cricket',
'https://www.theguardian.com/sport/us-sport',
'https://www.theguardian.com/uk/film',
'https://www.theguardian.com/games',
'https://www.theguardian.com/stage',
'https://www.theguardian.com/books',
'https://www.theguardian.com/music',
'https://www.theguardian.com/fashion',
'https://www.theguardian.com/uk/travel',
'https://www.theguardian.com/lifeandstyle/health-and-wellbeing',
'https://www.theguardian.com/profile/editorial',
'https://www.theguardian.com/global-development',
'https://www.theguardian.com/environment/wildlife',
'https://www.theguardian.com/uk/business'
]
for url in urls:
	strhtml = requests.Session().get(url)
	soup = BeautifulSoup(strhtml.text,'lxml')
	rtn = soup.find('script', {'data-schema':'ItemList'})
	for rt in rtn:
		# print(rt.strip())
		dic = eval(rt.strip())
		# print(dic.keys())
		# print(dic["itemListElement"])
		for u in dic["itemListElement"]:
			if 'url' in u:
				print(u['url'])
				crawlist.append(u['url'])
			else:
				newdic = u['item']
				for nu in newdic["itemListElement"]:
					print(nu['url'])
					crawlist.append(nu['url'])
			
print(len(crawlist))
crawlist = set(crawlist)
print(len(crawlist))
# os.system("pause");
print()
#craw text
baseline = 1200
crawfile = 'crawldata.txt'
if os.path.exists(crawfile):	os.remove(crawfile)

for url in crawlist:
	print(url)
	try:
		strhtml = requests.Session().get(url)
	except Exception:
		continue
	
	soup = BeautifulSoup(strhtml.text,'lxml')
	data = soup.select('div.content__article-body > p')

	print(len(data))
	with open(crawfile, 'a+', encoding='utf-8') as file:
		chang = 0
		for item in data:
			line = item.get_text()
			file.write(line)
			chang = len(line) + chang
			if chang > baseline:
				file.write('\n')
				chang = 0
		file.write('\n')

print("New work done!")