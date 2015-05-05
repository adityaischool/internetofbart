import requests,os,datetime,time
def uploadimages():
	url = "http://internetofbart.productfactory.me/upload"
	files = {'file1': open('temp.jpg', 'rb'),'file2': open('temp.jpg', 'rb'),'file3': open('temp.jpg', 'rb')}
	r = requests.post(url, files=files)

def uploadimagestest():
	url = "http://127.0.0.1:5000/upload"
	files = {'file1': open('temp.jpg', 'rb'),'file2': open('temp.jpg', 'rb'),'file3': open('temp.jpg', 'rb')}
	r = requests.post(url, files=files)
def uploadimagestest2():
	url = "http://internetofbart.productfactory.me/upload"
	files = {'file1': open('text.txt', 'rb'),'file2': open('text.txt', 'rb'),'file3': open('text.txt', 'rb')}
	r = requests.post(url, files=files)
def randome():
	li= os.listdir("static/uploads/")
	print li
	li.sort()
	print li
	print datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')

#randome()
uploadimagestest()