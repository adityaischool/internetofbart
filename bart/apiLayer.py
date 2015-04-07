import urllib2
import math
import json
import requests
from xml.etree import ElementTree
from datetime import datetime,time,date
from bart import geoDistance

def trimLoc(coord,precision):
	#print "cood",coord,"\n",(float(str(coord).split('.')[0]+"."+str(coord).split('.')[1][0:precision])
	return float(str(coord).split('.')[0]+"."+str(coord).split('.')[1][0:precision])

def placeMatches(lati,longi,latstat,longstat,precision):
	if (trimLoc(lati,precision)==trimLoc(latstat,precision))and(trimLoc(longi,precision)==trimLoc(longstat,precision)):
		return True
	else:
		return False

def getDataForUser(lati,longi,precision):
	#Key-MW9S-E7SL-26DU-VV8V
	apikey='MW9S-E7SL-26DU-VV8V'
	baseURL='http://api.bart.gov/api/stn.aspx?cmd=stns'
	data1={'key':apikey}
	r=requests.get(baseURL,params=data1)
	#r=requests.post(baseURL,data=data1)
	#r=requests.post(baseURL,data=data1)
	#print r
	tree = ElementTree.fromstring(r.content)
	#print str(tree.tag)
	#root=tree.getroot()
	#print root
	for childi in tree.getchildren():
		#print childi
		for child2 in childi.getchildren():
			latStat=child2.find("gtfs_latitude").text
			longStat=child2.find("gtfs_longitude").text
			#print "before pass",latStat,longStat
			if placeMatches(lati,longi,latStat,longStat,precision)==True:
				#print "found !!!"
				return child2.find("abbr").text
	return False

def getShortestStation(lati,longi):
	#Key-MW9S-E7SL-26DU-VV8V
	shortestStat=False
	apikey='MW9S-E7SL-26DU-VV8V'
	baseURL='http://api.bart.gov/api/stn.aspx?cmd=stns'
	data1={'key':apikey}
	r=requests.get(baseURL,params=data1)
	#r=requests.post(baseURL,data=data1)
	#r=requests.post(baseURL,data=data1)
	#print r
	tree = ElementTree.fromstring(r.content)
	print str(tree.tag)
	shortestDist=1000000
	#root=tree.getroot()
	#print root
	for childi in tree.getchildren():
		#print childi
		for child2 in childi.getchildren():
			latStat=child2.find("gtfs_latitude").text
			longStat=child2.find("gtfs_longitude").text
			#print "before pass",latStat,longStat
			newDist=geoDistance.distance_on_unit_sphere(lati,longi,latStat,longStat)*10000
			if newDist<shortestDist:
				#print "new shortest !!!    ",child2.find("abbr").text,"    ",newDist
				shortestStat = child2.find("abbr").text
				shortestDist=newDist
	return shortestStat

def getCurrentBartStation(latx,longx):
	stationAbbr=getDataForUser(latx, longx , 4)
	precision=4
	while(stationAbbr==False):
		#location is not a station
		print "not found"
		if precision==0:
			return False
		precision=precision-1
		stationAbbr=getDataForUser(latx,  longx , precision)
	print "station found ==== ", stationAbbr
	return stationAbbr

def getinComingTrainIDsForStation(abbr):
	nowhr,nowmin,counter=datetime.now().hour,datetime.now().minute,0
	trainlist=[]
	loadFactor=0
	apikey='MW9S-E7SL-26DU-VV8V'
	baseURL='http://api.bart.gov/api/sched.aspx?cmd=stnsched'
	data1={'key':apikey,'orig':abbr}
	r=requests.get(baseURL,params=data1)
	#print r
	tree = ElementTree.fromstring(r.content)
	#print str(tree.tag)
	#root=tree.getroot()
	print 'tree',tree
	for childi in tree.find('station').findall('item'):
		#print childi.tag,childi.attrib
		respitem=dict(childi.attrib)
		timeEntry = str(respitem['origTime'].split(' ')[0]).split(':')
		entryhrs,entrymins,entryM = int(timeEntry[0]),int(timeEntry[1]),str(respitem['origTime'].split(' ')[1])
		if nowhr>11 and entryM=="PM" and entryhrs<12:
			entryhrs=entryhrs+12
		#print entryhrsS,nowhr
		if entryhrs>nowhr or (entryhrs==nowhr and entrymins>nowmin):
			counter=counter+1
			#trainID='Train-'+str(respitem['line'].split(' ')[1])+'-'+respitem['trainIdx']
			trainID=str(respitem['line'].split(' ')[1])+'-'+respitem['trainIdx']+"-"+str(date.today().day)+"-"+str(date.today().month)+"-"+str(date.today().year)
			print "Train ID is - ",trainID
			loadFactor=getLoadFactor(abbr,trainID)
			newDict={'loadFactor':loadFactor,'trainID':trainID,'trainHeadStation':respitem['trainHeadStation'],'origTime':respitem['origTime']}
			trainlist.append(newDict)
			if(counter>4):
				print "About to return !! --- ", trainlist
				return trainlist

	return False


def getLoadFactor(abbr,trainID):
	apikey='ZMVV-JDE7-IQ9Q-DT35'
	routePad=trainID.split('-')[0]
	routePad2=trainID.split('-')[1]
	baseURL='http://api.bart.gov/api/sched.aspx?cmd=load'
	if(len(routePad)==1):
		routePad='0'+routePad
	if(len(routePad2)==1):
		routePad2='0'+routePad2
	print "load factor with -", abbr+routePad+trainID.split('-')[1]
	data1={'key':apikey, 'ld1':abbr+routePad+routePad2,'st':'w'}
	r=requests.get(baseURL,params=data1)
	#r=requests.post(baseURL,data=data1)
	#r=requests.post(baseURL,data=data1)
	#print r
	try:
		tree = ElementTree.fromstring(r.content)
		print "respinse",r.content
		node=dict(tree.find('load').find('request').find('leg').attrib)
		retDict={'1':'Light','2':'Medium','3':'Heavy'}
		return retDict[node['load']]
	except ValueError:
		return "Unknown"
