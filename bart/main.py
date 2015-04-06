from urllib2 import Request, urlopen, URLError
import json
#https://www.eventbriteapi.com/v3/events/search/?token=BKKRDKVUVRC5WG4HAVLT&location.latitude=37&location.longitude=-122&location.within=20km

def getRequest(Lat,Long,Rad):
	Lat=str(Lat)
	Long=str(Long)

	reqString='https://www.eventbriteapi.com/v3/events/search/?token=BKKRDKVUVRC5WG4HAVLT&location.latitude='+Lat+'&location.longitude='+Long+'&location.within=1.42m'
	try:
		request = Request(reqString)
		response = urlopen(request)
		data = response.read()
		#print kittens
		m=json.loads(data)
		
		print m
		#print kittens[559:1000]
	except URLError, e:
		print 'No kittez. Got an error code:', e


getRequest(37, 122, 1)