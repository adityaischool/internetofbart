import requests
def uploadimages():
	url = "http://internetofbart.productfactory.me/upload"
	files = {'file1': open('background.jpg', 'rb'),'file2': open('newPicture.jpg', 'rb'),'file3': open('result.jpg', 'rb')}
	r = requests.post(url, files=files)

def uploadimagestest():
	url = "http://127.0.0.1:5000/upload"
	files = {'file1': open('text.txt', 'rb')}
	r = requests.post(url, files=files)

uploadimagestest()