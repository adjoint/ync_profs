# -*- coding: utf-8 -*-


import urllib2
import time
import copy
import csv

er = open('places_errors.txt', 'w')

link = "http://maps.googleapis.com/maps/api/geocode/json?address="
addition = "Novosibirsk"
html = urllib2.urlopen(link + addition)
data = html.readlines()
for i in range(len(data)):
	#print data[i]
	if 'location" : {' in data[i]:
		lng = data[i+2].replace(" ", "")[6:].strip("\n")
		#print lng
		lat = data[i+1].replace(" ", "")[6:].strip(",\n")
		#print lat
		break
		if len(lng) > 0 and len(lat) > 0:
			tup = "[" + str(lng) + "," + str(lat) + "],"
		else:
			tup = "[CHECK ME " + addition + "],"
			er.write(str(addition) + "\n")

#print (lng, lat)

er.close()