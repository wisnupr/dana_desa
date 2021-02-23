import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def ambil(url):
	req = requests.get(url, verify=False)
	dsoup = BeautifulSoup(req.content)
	return dsoup

# load url root
with open('urlroot.json', "r") as read_it:
	data = json.load(read_it)

a = 0
# create header
keyd = ['uraian','anggaran']
dx = []
for u in data:
	if u['link'] is not None:
		url0 = u['link']
		n=ambil(url0)
		kkk = []
		try:
			# x grup data level wilayah
			x = {}
			for i in n.findAll('tr')[:4]:
				x[i.text.split('\n')[1]] = str(i.text.split('\n')[-2])
			x['tahun'] = '2020'
			x['url'] = url0
			for i in n.findAll('div',{'class':'color-single nk-green'}):
				x[i.find('h2').string] = i.find('span').string
			# data - change list table for another data
			# g = []
			for i in n.findAll('table')[1].findAll('tr')[1:]:
				g = []
				for h in i.findAll('td'):
					# cleaning \r\n
					w = h.text.replace('\r\n',' ')
					g.append(w.replace('\n',''))
					# print(w)
				kkk.append(list(x.values())+g)
				print(kkk)
		except:
			kk = list(x.values())
			kkk.append(kk)
		# grup data
		key1 = list(x.keys())+keyd
		for l in kkk:
			data = dict(zip(key1,l))
			dx.append(data)

	a = a + 1
	print('berhasil merampas '+str(a)+' data: '+str(u['id_desa']))
	
with open('training5.json', 'w', encoding='utf-8') as f:
	json.dump(dx, f, ensure_ascii=False, indent=4)
print(kkk)

# with open('training6.csv', 'w') as o_f:
#     d_w = csv.DictWriter(o_f, key1)
#     d_w.writeheader()
#     d_w.writerows(dx)