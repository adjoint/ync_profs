# -*- coding: utf-8 -*-
import csv
import copy 
import urllib2
import time
import requests


print 5

with open("profs2.txt") as f:
    content = f.readlines()
#print content[:100]

m = open("markers3.txt", "w")
p = open("polylines3.txt", "w")

new_content = []
to_add = []

for el in content:
  if "Beginning:" in el:
    if to_add != []:
      name = to_add[0].strip("\n")
      discipline = to_add[1].strip("\n")
      description = ""
      j = 0
      for i in range(2, len(to_add)):
        if "Places mapped:" not in to_add[i]:
          description += to_add[i]
        else:
          j = i
          break
      description = description.strip("\n")
      places = []
      for i in range(j+1, len(to_add)):
        if to_add[i] != "\n":
          places.append(to_add[i].strip("\n"))
      new_content.append([name, discipline, description, places])
      to_add = []
  else: 
    to_add.append(el)

#print new_content[:5]

colorSC = "#337AFF"
colorSS = "#F7F7F7"
colorHU = "#FF8D33"

str1 = "{type: 'Feature',geometry: {type: 'Point',coordinates: ["
str2 = "]},properties: {'description':'"
str3 = "','marker-color': '"
str4 = "','marker-size': 'medium','marker-symbol': 'college'} },"

str5 = "var line_points"
str6 = " = ["
str7 = "];"

str8 = "var polyline_options"
str9 = " = {color: '"
str10 = "'};"

str11 = "var polyline" 
str12 = "= L.polyline(line_points"
str13 = ", polyline_options"
str14 = ").addTo(map);"



er = open('places_errors3.txt', 'w')
coords = open('coords3.txt', 'w')

link = "http://maps.googleapis.com/maps/api/geocode/json?address="


i = 0
for el in new_content:
  name = el[0]
  discipline = el[1]
  desc = el[2]
  description = "<b>" + str(name) + "</b><br><i>" + str(discipline) + "</i><hr>" + str(desc)
  places = el[3]
  if discipline[:7] == "Science":
    color = colorSC
  elif "Social Science" in discipline:
    color = colorSS
  elif "Humanities" in discipline:
    color = colorHU
  points_array = ""
  num = 0
  needed = "CHECK ME " + str(places[0])
  for pl in places:
    addition = pl.replace(" ", "%20")
    tup = ""
    lng = ""
    lat = ""
    try:
      """html = urllib2.urlopen(link + addition)
      data = html.readlines()
      for i in range(len(data)):
      #print data[i]
        if 'location" : {' in data[i]:
          lng = data[i+2].replace(" ", "")[6:].strip("\n")
          #print lng
          lat = data[i+1].replace(" ", "")[6:].strip(",\n")
          #print lat
          break"""
      response = requests.get(link + addition)

      resp_json_payload = response.json()
      try:
        lat = str(resp_json_payload['results'][0]['geometry']['location']['lat'])
        lng = str(resp_json_payload['results'][0]['geometry']['location']['lng'])
      except IndexError:
        er.write(str(pl) + "\n")
      if len(lng) > 0 and len(lat) > 0:
        tup = str(lng) + "," + str(lat)
        if num == 0:
          needed = tup
        coords.write(str(pl) + "," + str(tup) + "\n")
      else:
        tup = "[CHECK ME " + pl + "]"
        #er.write(str(pl) + "\n")
      num +=1
      i += 1
      print i
    except urllib2.HTTPError as err:
      print "ERROR " + str(addition) + " " + str(err.code) 
    
    points_array = points_array + tup + ","
  points_array = points_array.strip(",")
  toM = str1 + str(needed) + str2 + str(description) + str3 + str(color) + str4
  m.write(toM + "\n")
  toP = str5 + str(i) + str6 + points_array + str7 + "\n" + str8 + str(i) + str9 + str(color) + str10 + "\n" + str11 + str(i) + str12 + str(i) + str13 + str(i) + str14
  p.write(toP + "\n")



"""while i < len(content):
  name = content[i]
  discipline = content[i+1]
  desc = content[i+2]
  description = "<b>" + str(name) + "</b><br><i>" + str(discipline) + "</i><hr>" + str(desc)
  places = content[i+4]
  if "Places mapped:" not in places:
    print "ERROR in PLACES MAPPED"
  if discipline[:7] == "Science":
    color = colorSC
  elif "Social Science" in discipline:
    color = colorSS
  elif "Humanities" in discipline:
    color = colorHU
  else:
    print "ERROR: " + str(name)
  toM = str1 + "[]" + str2 + str(description) + str3 + str(color) + str4
  m.write(toM + "\n")
  i = i+5
  line = "can"
  points_array = ""
  while line!="\n" and i < len(content):
    line = content[i]
    if line!="\n":
      points_array = points_array + str(i)
      i += 1
  toP = str5 + str(i) + str6 + points_array + str7 + "\n" + str8 + str(i) + str9 + str(color) + str10 + "\n" + str11 + str(i) + str12 + str(i) + str13 + str(i) + str14
  p.write(toP + "\n")"""












er.close()
coords.close()
m.close()
p.close()