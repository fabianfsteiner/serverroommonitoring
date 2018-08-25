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
import RPi.GPIO as GPIO

#destination for the XML File
path = '/var/www/html/xml/water.xml'
#set up logging
logFormatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
rootLogger = logging.getLogger()
fileHandler = logging.handlers.RotatingFileHandler('/var/log/water/water.log',maxBytes=1000000,backupCount=5)
fileHandler.setFormatter(logFormatter)
console = logging.StreamHandler()
rootLogger.addHandler(fileHandler)
rootLogger.addHandler(console)
rootLogger.setLevel(logging.INFO)

#Pin Modus setzen
GPIO.setmode(GPIO.BCM)

#Inputs setzen
pins = list()
with open('/home/pi/pinconfig/water.cfg', mode= 'r') as file:
	for line in file:
		pins = line.split(',')
		logging.info("GPIOS are: " + str(pins))
		for pin in pins:
			GPIO.setup(int(pin), GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

#find out local ip address (we want to tell the recievers the name of the system)
local = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]

#header - figure out system name
sql = "select name from messsystem where ip = '%s';" % (local)
try:
	db = pymysql.connect(host='localhost', user='webuser', password='La4R2uyME78hAfn9I1pH',db='serverraum_temperaturueberwachung',autocommit=True)
	cursor = db.cursor()
	logging.info("Connected to database")
	logging.debug(sql)
	cursor.execute(sql)
	systemname = cursor.fetchone()[0]
	logging.info("SystemName is: " +systemname)
	db.close()
except Exception as e:
	logging.error(e)
	sys.exit()

waterprefix = systemname.split(' ')[1]

while True:
	#connection stays open until an error
	try:
		db = pymysql.connect(host='localhost', user='webuser', password='La4R2uyME78hAfn9I1pH',db='serverraum_temperaturueberwachung',autocommit=True)
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
			sql = "insert into messung (zeit , fk_sensorID, wasser) values"
			out = '<?xml version="1.0" encoding="ISO-8859-1" ?><?xml-stylesheet type="text/xsl" href="./actualwater.xsl"?><monitoring>'
			now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			logging.debug("beginning")
			#save measurements to the database and produce xml, missing sensors will be created automatically
			for pin in pins:
				pin = int(pin)
				logging.debug("reading GPIO: " + str(pin))
				sk = 'wasser'+ str(waterprefix) + str(pin)
				try:
					logging.debug(str(GPIO.input(pin)))
					if str(GPIO.input(pin)) == "1":
						water = 1
						logging.warning("water signal on GPIO " + str(pin))
					else:
						water = 0
						logging.info("it's dry at GPIO " + str(pin))
					sql = sql + " ('%s',func_getSID('%s'), %d)," % (now, sk, water)
					for sensor in sensoren:
						if str(sensor[0]) == sk:
							logging.debug("here")
							out= out + '<sensor name = "'+str(sensor[2])+'"><id>'+str(sensor[1])+'</id><level>'+str(water)+'</level><zeit>'+now+'</zeit></sensor>'
				except Exception as e:
					logging.error(e)
			out = out + "</monitoring>"
			logging.debug(out)
			with open(path, "w") as xml:
				print(out, file=xml)
			logging.info("XML File sucessfully generated")
			logging.debug(sql[:-1] + ";")
			cursor.execute(sql[:-1] + ";")
			logging.info("Data sucessfully inserted into database")
			#wait for 60 seconds
			time.sleep(60)
		except Exception as g:
			logging.error(g)
			logging.info("Database Connection will be reopened")
			db.close()
			break