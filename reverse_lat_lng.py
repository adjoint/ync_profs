# -*- coding: utf-8 -*-
import csv
import copy 
import urllib2
import time
import requests

with open("polylines.txt") as f:
    content = f.readlines()

n = open("new_polylines.txt", "w")

for line in content:
	new_line = line.split("[[")
	#print new_line
	if len(new_line) > 1:
		str1 = new_line[0] + "[["
		str2 = new_line[1].strip("]];\n")
		coords = str2.split("],[")
		#print coords
		to_write = str1
		for c in coords:
			tup = c.split(",")
			new_tup = str(tup[1]) + "," + str(tup[0])
			to_write += new_tup + "],["
		to_write = to_write[:-2]
		to_write += "];"
		n.write(str(to_write) + "\n")
	else:
		n.write(str(line))

n.close()