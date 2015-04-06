import urllib2
import math
import json
import requests
from xml.etree import ElementTree
from datetime import datetime,time,date

def getLoadFactor(abbr,trainID):
	apikey='ZMVV-JDE7-IQ9Q-DT35'
	routePad=trainID.split('-')[0]
	baseURL='http://api.bart.gov/api/sched.aspx?cmd=load'
	if(len(routePad)==1):
		routePad='0'+routePad
	print "load factor with -", abbr+routePad+trainID.split('-')[1]
	data1={'key':apikey, 'ld1':abbr+routePad+trainID.split('-')[1],'st':'w'}
	r=requests.get(baseURL,params=data1)
	#r=requests.post(baseURL,data=data1)
	#r=requests.post(baseURL,data=data1)
	#print r
	tree = ElementTree.fromstring(r.content)
	print "respinse",r.content
	node=dict(tree.find('load').find('request').find('leg').attrib)
	return node['load']

