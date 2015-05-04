from flask import render_template,request,session,redirect,jsonify,Response
from flask import url_for
from bart import app
import urllib2
import math
import json
import requests
from bart import apiLayer,asBaseLayer
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
	if request.method == 'POST':
		f = request.files['file1']
		f2 = request.files['file2']
		f3 = request.files['file3']
		print "file recieved"
		f.save('bart/static/uploads/background.jpeg')
		f2.save('bart/static/uploads/newPicture.jpeg')
		f3.save('bart/static/uploads/result.jpeg')
		return '200'
	else:
		return 'Upload Page'
