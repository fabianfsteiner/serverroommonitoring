#!/usr/bin/python
# -*- coding: utf-8 -*-
import pymysql
import sys
import glob
import datetime
import time
import logging
import logging.handlers
import socket

#destination for the XML File
path = '/var/www/html/xml/temp.xml'
#set up logging
logFormatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
rootLogger = logging.getLogger()
fileHandler = logging.handlers.RotatingFileHandler('/var/log/1wire/1wire.log',maxBytes=1000000,backupCount=5)
fileHandler.setFormatter(logFormatter)
console = logging.StreamHandler()
rootLogger.addHandler(fileHandler)
rootLogger.addHandler(console)
rootLogger.setLevel(logging.DEBUG)

#find out local ip address (we want to tell the recievers the name of the system)
local = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]

while True:
	#connection stays open until an error
	try:
		db = pymysql.connect(host='localhost', user='webuser', password='t5sLhtva6Ev8xjptFpGhu2zupsy64sgTndg',db='serverraum_temperaturueberwachung',autocommit=True)
		cursor = db.cursor()
		logging.info("Connected to database")
	except Exception as e:
		logging.error(e)
		continue
	while True:
		#connect to database
		try:
			cursor.execute("select sensorKennung, sensorID, sensorPosition from sensor where fk_systemID = (select systemID from messsystem where ip = '"+local+"') order by sensorName;")
			sensoren = cursor.fetchall()
			logging.debug(sensoren)
			# read 1-wire slaves list
			paths = glob.glob(r'/sys/devices/w1_bus_master1/10-*')
			sql = "insert into messung (zeit , fk_sensorID, temp) values"
			out = '<?xml version="1.0" encoding="ISO-8859-1" ?><?xml-stylesheet type="text/xsl" href="./actualtemp.xsl"?><monitoring>'
			now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			logging.debug("beginning")
			#save measurements to the database and produce xml, missing sensors will be created automatically
			for filename in paths:
				logging.debug("reading file: " + filename)
				try:
					with open(filename + '/w1_slave', "r") as file:
						filecontent = file.readlines()
						stringvalue = filecontent[1].split(" ")[9]
						temperature = str(float(stringvalue[2:]) / 1000.0)
						logging.debug(str(filename) + ": " + temperature + "°C")
						sql = sql + " ('%s',func_getSID('%s'), %s)," % (now,str(filename).split('/')[4], temperature)
						for sensor in sensoren:
							if str(sensor[0]) == str(filename).split('/')[4]:
								out= out + '<sensor name = "'+str(sensor[2])+'"><id>'+str(sensor[1])+'</id><temp>'+str(temperature)+'</temp><zeit>'+now+'</zeit></sensor>'
				except Exception as e:
					logging.error(e, "damn")
			logging.debug(sql[:-1] + ";")
			cursor.execute(sql[:-1] + ";")
			logging.info("Data successfully inserted into database")
			out = out + "</monitoring>"
			logging.debug(out)
			with open(path, "w") as xml:
				print(out, file=xml)
			logging.info("XML File successfully generated")
		except Exception as g:
			logging.error(g)
			logging.info("Database Connection will be reopened")
			db.close()
			break