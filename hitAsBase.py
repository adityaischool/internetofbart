import requests

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

urlis="http://russet.ischool.berkeley.edu:8080/query/"
data1={'startTime':'2015-02-10T15:04:55Z', 'endTime':'2015-03-30T15:04:55Z'}
#r=requests.get(urlis,params=data1)
#r=requests.post(urlis,params=data1)
r=requests.get("http://russet.ischool.berkeley.edu:8080/query/")

#print r.content()
print r.json()