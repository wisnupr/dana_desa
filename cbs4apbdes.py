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

with open('urlroot.json', "r") as read_it:
	data = json.load(read_it)

h = 0
keyd = ['kode_rekening','uraian','anggaran', 'sumber_dana']
dx = []
for u in data:
	if u['link'] is not None:
		url0 = u['link']
		n=ambil(url0)
		kkk = []
		try:
			x = {}
			# y = []
			for i in n.findAll('tr')[:4]:
				x[i.text.split('\n')[1]] = str(i.text.split('\n')[-2])
			x['tahun'] = '2020'
			x['url'] = url0
			for i in n.findAll('div',{'class':'accordion-stn mg-t-30'})[0].findAll('tr')[:]:
				g = []
				for h in i.findAll('td'):
					g.append(h.text)
				kkk.append(list(x.values())+g)
				print(kkk)
		except:
			kk = list(x.values())
			kkk.append(kk)

		key1 = list(x.keys())+keyd
		for l in kkk:
			data = dict(zip(key1,l))
			dx.append(data)
with open('training14.csv', 'w') as o_f:
    d_w = csv.DictWriter(o_f, key1)
    d_w.writeheader()
    d_w.writerows(dx)