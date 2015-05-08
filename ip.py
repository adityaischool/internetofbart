#!usr/bin/python

import subprocess
import threading
import time


lst = []

class Thread(threading.Thread):

	devnull = open('/dev/null', 'w')

	def __init__(self, threadID, name, ip):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.ip = ip

	def run(self):
		global lst

		print "Starting " + self.name		

		result = subprocess.call(["ping", "-n","1", "-w", "2000", self.ip], stdout=Thread.devnull)
		

		if result == 0:
			lst.append([self.threadID, "IP address " + self.ip + " is reachable."])

		elif result == 1:
			lst.append([self.threadID, "IP address " + self.ip + " is unreachable."])


def main():

	address = 0

	try:
		address = raw_input("Please enter your IP address:")

		addressSplit = address.split('.')

		print addressSplit

		for i in addressSplit:
			if int(i) > -1:
				continue
			else:
				print "not a valid IP address!"
				break

		print "valid address!"


	except:
		print "not a valid IP address!"

	print "Pinging all addresses in neighborhood", ".".join(addressSplit[:3])

	devnull = open('/dev/null', 'w')

	neighborhood = ".".join(addressSplit[:3])
	
	startTime = time.time()

	temp = {}

	for i in range(256):

		name = "thread"+str(i)

		name = Thread(i, "thread"+str(i), neighborhood+'.'+str(i))

		temp[i] = name

		name.start()
	

	f = open('HW10.script.jones.txt', 'rw+')

	for i in temp:
		temp[i].join()
	

	endTime = time.time()

	runTime = endTime - startTime


	sortedList = sorted(lst)

	print 

	f.readlines()

	f.write('\r\n\r\n\r\n')
	f.write('------THREADED OUTPUT------')
	f.write('\r\n\r\n')

	for i in sortedList:
		print i[1]
		f.write(i[1])
		f.write('\r\n')

	print
	print "Run Time = ", runTime, "seconds"
	f.write("\r\nRun Time = " + str(runTime) + " seconds.")

	f.close()


if __name__ == '__main__':
	main()