import requests
from datetime import datetime,time,timedelta
import json

def pushtobase(index):
	print "index to write = ",index
	print "reading density model, and rating"
	densityValues=readIndex(index)
	startTime=datetime.utcnow().isoformat()[0:-7] + 'Z'
	density=densityValues['density']
	crowded="Low Crowding"
	if(density>7):
		crowded="Overcrowded"
	elif density>4:
		crowded="Medium Crowding"
	train_density_index=2
	payload={"actor": {"displayName": "BARTtrain","id": "1","objectType": "train"},"verb": "checkin","published": startTime,"status": "completed","object": {"displayName":"Car1","dataFields": {"train_length": 1,"train_route": 7,"train_index": 72,"route_start": "SFIA","route_end": "PITT","station_previous": "ROCK","station_next": "ORIN","car_1": {"car_density_index": density,"overcrowded": crowded}},"objectType": "trainRecord"},"target" : {"url": "http://example.org/blog/","objectType": "blog","id": "tag:example.org,2011:abc123","displayName": "Berkeley"}}
	url="http://russet.ischool.berkeley.edu:8080/activities"
	headers = { 'Content-Type': 'application/stream+json' }
	try:
		r = requests.post(url, data=json.dumps(payload), headers=headers)
		print r
	except Exception as e:
		print e


def readIndex(index):
	#build a model to convert raw pixel counts into index
	scale=float(index)
	minScale=100
	maxScale=5000000
	newindex=(scale-minScale)*10/(maxScale-minScale)
	print newindex
	if index<minScale:
		return {'density':0}
	elif index>maxScale:
		return {'density':10}
	else:
		print (scale-minScale)*10/(maxScale-minScale)
		return {'density':int(round((scale-minScale)*10/(maxScale-minScale)))}

def readfrombase(trainid):
	print "Inside getDataForTrain  ", trainid
	#2015-04-28T08:35:53.000Z
	respList=[]
	result=[]
	startTime=datetime.utcnow().isoformat()[0:-7] + '.000Z'
	endTime=(datetime.utcnow() + timedelta(hours=-15)).isoformat()[0:-7] + '.000Z'
	print startTime,endTime
	urlis="http://russet.ischool.berkeley.edu:8080/query/"
	data1={'startTime':str(startTime), 'endTime':str(endTime)}
	#r=requests.get(urlis,params=data1)
	r=requests.get(urlis)
	try:
		result=json.loads(r.content)
	except ValueError:
		print "AS Base seems down - "
	#print result
	#print result['items'][2]['object']
	if('items' in result):
		for objects in result['items']:
			if type(objects['actor'])==type({}):
				#print objects
				if (objects['actor']['displayName']=='BARTtrain' and objects['actor']['id']==trainid):
					respList.append({'id':objects['actor']['id'],'car_1':[objects['object']['dataFields']['car_1']]})
					return respList
	else:
		return ['Car DATA not found']


def newreadfrombase(trainid):
	print "Inside getDataForTrain  ", trainid
	#2015-04-28T08:35:53.000Z
	respList=[]
	result=[]
	startTime=datetime.utcnow().isoformat()[0:-7] + '.000Z'
	endTime=(datetime.utcnow() + timedelta(hours=-15)).isoformat()[0:-7] + '.000Z'
	print startTime,endTime
	car1=False
	car2=False
	seat=False
	urlis="http://russet.ischool.berkeley.edu:8080/query/"
	data1={'startTime':str(startTime), 'endTime':str(endTime)}
	#r=requests.get(urlis,params=data1)
	r=requests.get(urlis)
	try:
		result=json.loads(r.content)
	except ValueError:
		print "AS Base seems down - "
	#print result
	#print result['items'][2]['object']
	if('items' in result):
		for objects in result['items']:
			if type(objects['actor'])==type({}):
				#print objects
				if (objects['actor']['displayName']=='BARTtrain' and objects['actor']['id']=="1" and car1=False):
					respList.append({'id':objects['actor']['id'],'car_1':[objects['object']['dataFields']['car_1']]})
					car1=True
				if (objects['actor']['displayName']=='BARTtrain' and objects['actor']['id']=="2" and car1=False):
					respList.append({'id':objects['actor']['id'],'car_2':[objects['object']['dataFields']['car_1']]})	
					car2=True
				if car1 and car2:
					return respList
	else:
		return ['Car DATA not found']

def newpushtobase(index,carid):
	print "index to write = ",index
	print "reading density model, and rating"
	densityValues=readIndex(index)
	startTime=datetime.utcnow().isoformat()[0:-7] + 'Z'
	density=densityValues['density']
	crowded="Low Crowding"
	if(density>7):
		crowded="Overcrowded"
	elif density>4:
		crowded="Medium Crowding"
	train_density_index=2
	payload={"actor": {"displayName": "BARTtrain","id": carid,"objectType": "train"},"verb": "checkin","published": startTime,"status": "completed","object": {"displayName":"Car1","dataFields": {"train_length": 1,"train_route": 7,"train_index": 72,"route_start": "SFIA","route_end": "PITT","station_previous": "ROCK","station_next": "ORIN","car_1": {"car_density_index": density,"overcrowded": crowded}},"objectType": "trainRecord"},"target" : {"url": "http://example.org/blog/","objectType": "blog","id": "tag:example.org,2011:abc123","displayName": "Berkeley"}}
	url="http://russet.ischool.berkeley.edu:8080/activities"
	headers = { 'Content-Type': 'application/stream+json' }
	try:
		r = requests.post(url, data=json.dumps(payload), headers=headers)
		print r
	except Exception as e:
		print e
#print readfrombase('1')
#print readIndex(1000000)
#pushtobase(2500000)
newpushtobase(1500000,"1")
print newreadfrombase("1")
