from flask import render_template,request,session,redirect,jsonify,Response
from flask import url_for
from bart import app
import urllib2
import math
import json,os,requests,os,datetime,time
from bart import apiLayer,asBaseLayer,newASWrapper
from flask import Response
#import request

@app.route('/', methods=['GET', 'POST'])
def land():
	return render_template("newindex.html")
'''@app.route("/")
def home():
    resp = flask.Response("Foo bar baz")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp'''

@app.route('/activitynotify', methods=['GET', 'POST'])
def activitynotify():
	print "request recd" + request.content
	return Response("Foo bar baz")


@app.route('/_postLocation', methods=['GET', 'POST'])
def postLocation():
	lati=request.args.get('lati')
	longi=request.args.get('longit')
	finalDataStruct=[]
	print "hit post locations with params",lati,longi
	#stationCode=apiLayer.getCurrentBartStation(lati,longi)
	stationCode=apiLayer.getShortestStation(lati,longi)
	print "Station Code is - ", stationCode
	if(stationCode==False):
		#user not in station -- route to page
		print "okay" 
	else:
		dictionaryOfIncomingTrains=apiLayer.getinComingTrainIDsForStation(stationCode)
		print dictionaryOfIncomingTrains
		'''[{'trainHeadStation': 'RICH', 'origTime': '4:47 PM', 'trainID': 'Train-3-49'}, 
		{'trainHeadStation': 'FRMT', 'origTime': '4:48 PM', 'trainID': 'Train-4-50'}, 
		{'trainHeadStation': 'RICH', 'origTime': '4:54 PM', 'trainID': 'Train-8-44'}, 
		{'trainHeadStation': 'MLBR', 'origTime': '4:55 PM', 'trainID': 'Train-7-51'}, 
		{'trainHeadStation': 'RICH', 'origTime': '5:02 PM', 'trainID': 'Train-3-50'}]
'''
		for train in dictionaryOfIncomingTrains:
			print "fetching ACTIVITY!!!!","\n"
			trainTemp=train.copy()
			trainTemp['carData']=asBaseLayer.getDataForTrain(train)
			finalDataStruct.append(trainTemp)
			print trainTemp

		#here iterate over each list item and hit ASbase
		print {'dicto':finalDataStruct,'stationabbr':stationCode}
		return json.dumps({'dict':finalDataStruct,'stationabbr':stationCode})

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	print "hit upload"
	if request.method == 'POST':
		f = request.files['file1']
		f2 = request.files['file2']
		f3 = request.files['file3']
		imgid=datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
		print "files recieved -",imgid , "path  ",
		path1=os.path.dirname(__file__)
		print "filess  ",f,f2,f3
		print os.path.join(path1,'static/uploads/'+str(imgid)+'-b.jpeg')
		try:
			f.save(os.path.join(path1,'static/uploads/'+str(imgid)+'-b.jpeg'))
			f2.save(os.path.join(path1,'static/uploads/'+str(imgid)+'-n.jpeg'))
			f3.save(os.path.join(path1,'static/uploads/'+str(imgid)+'-r.jpeg'))
		except Exception as e:
			print e
		return '200'
	else:
		return 'Upload Page'

@app.route('/images', methods=['GET', 'POST'])
def images():
	path1=os.path.dirname(__file__)
	filelist=os.listdir(os.path.join(path1,'static/uploads/'))
	filelist.sort(reverse=True)
	imagelist=[]
	tempobj={}
	for i in filelist:
		if '-b' in i:
			tempobj['b']='/static/uploads/'+i
		elif '-n' in i:
			tempobj['n']='/static/uploads/'+i
		elif '-r' in i:
			tempobj['r']='/static/uploads/'+i
			imagelist.append((tempobj))
			tempobj={}
	print imagelist
	return render_template("stream.html",imagelist=imagelist)


@app.route('/station1', methods=['GET', 'POST'])
def station1():
	retDict=newASWrapper.newreadfrombase(1)
	print "RETURN !!!!!",retDict
	density=0
	seat=False
	crowd1='/static/images/green.png'
	seat1='/static/images/green.png'
	crowd2='/static/images/green.png'
	seat2='/static/images/green.png'
	for car in retDict:
		if car['id']==1 or car['id']=='1':
			density=car['car_1'][0]['car_density_index']
			seat=car['seat']
			if density>7:
				crowd1='/static/images/red.png'
			elif density>4:
				crowd1='/static/images/orange.png'
			else:
				crowd1='/static/images/green.png'
			if seat==False:
				seat1='/static/images/green.png'
			else:
				seat1='/static/images/red.png'
		if car['id']==2 or car['id']=='2':
			density=car['car_2'][0]['car_density_index']
			seat=car['seat']
			if density>7:
				crowd2='/static/images/red.png'
			elif density>4:
				crowd2='/static/images/orange.png'
			else:
				crowd2='/static/images/green.png'
			if seat==False:
				seat2='/static/images/green.png'
			else:
				seat2='/static/images/red.png'

	return render_template("station1.html",crowd1=crowd1,seat1=seat1,crowd2=crowd2,seat2=seat2)