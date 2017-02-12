import urllib2
import os
import threading, time

BUFFER_SIZE = 100
requested_file = raw_input("File name> ")
path = "/home/freddie/IdeaProjects/networking/Assignment2/text_files"
try:
	print "1"
	f = urllib2.urlopen("http://192.168.43.85:50009/"+requested_file)
	print f
	if not os.path.exists(path):
		os.makedirs(path)

	this_file = open(os.path.join(path,requested_file), "w+")
	print "3"

	this_buffer = f.read(BUFFER_SIZE)
	print "4"

	while this_buffer != "":
		this_file.write(this_buffer)
		this_buffer = f.read(BUFFER_SIZE)
		print "buffer"

	f.close()
	this_file.close()

except urllib2.URLError:
	print "nope"
