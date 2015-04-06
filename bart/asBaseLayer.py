import requests
from datetime import datetime,time,timedelta
import json



def advancedQuery(startTime,endTime):
	r=requests.get("http://russet.ischool.berkeley.edu:8080/query/")
	print r.json()	
	urlis="http://russet.ischool.berkeley.edu:8080/query/"
	data1={'startTime':'2013-02-10T15:04:55Z', 'endTime':'2011-02-10T15:04:55Z'}
	r=requests.get(urlis,params=data1)
	print r.json()

def simpleQuery():
	r=requests.get("http://russet.ischool.berkeley.edu:8080/query/")
	print r.json()


#2011-02-10T15:04:55Z
def sampleQuery():
	urlis="http://russet.ischool.berkeley.edu:8080/query/"
	data1={'startTime':'2015-02-10T15:04:55Z', 'endTime':'2015-03-30T15:04:55Z'}
	#r=requests.get(urlis,params=data1)
	#r=requests.post(urlis,params=data1)
	r=requests.get("http://russet.ischool.berkeley.edu:8080/query/")

#print r.content()
	print r.json()

def getRoutesForStation():
	print "place"

#simpleQuery()

def getDataForTrain(train):
	print "Inside getDataForTrain  ", train['trainID']
	respList=[]
	result=[]
	startTime=datetime.utcnow().isoformat()[0:-7] + 'Z'
	endTime=(datetime.utcnow() + timedelta(hours=-200)).isoformat()[0:-7] + 'Z'
	#print startTime,endTime
	urlis="http://russet.ischool.berkeley.edu:8080/query/"
	data1={'startTime':str(startTime), 'endTime':str(endTime)}
	#r=requests.get(urlis,params=data1)
	r=requests.get(urlis)
	try:
		result=json.loads(r.content)
	except ValueError:
		print "AS Base seems down - "

	#print result['items'][2]['object']
	if('items' in result):
		for objects in result['items']:
			if type(objects['actor'])==type({}):
				if (objects['actor']['displayName']=='BARTtrain' and objects['actor']['id']==train['trainID']):
					respList.append({'id':objects['actor']['id'],'car_1':[objects['dataFields']['car_1']],'car_2':[objects['dataFields']['car_2']]})
		print "AS Base result - ", respList
		return respList
	else:
		return ['Car DATA not found']


def postSubscriber():
	payload={"userID" : "BART-WebApp-LocalHost-AditUNIX","channels" : [{"type" : "URL_Callback", "data" : "http://example.org/"}]}
	url= "http://russet.ischool.berkeley.edu:8080/users"
	headers = { 'Content-Type': 'application/json' }
	r = requests.post(url, data=json.dumps(payload), headers=headers)
	print r

	#getDataForTrain({})
#postSubscriber()

# 	2015-04-01T20:26:39.000Z