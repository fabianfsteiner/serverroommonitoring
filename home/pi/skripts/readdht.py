#!/usr/bin/python
# -*- coding: utf-8 -*-

#this skript was designed to work with python2
import pymysql
import sys
import Adafruit_DHT
import datetime
import time
import logging
import logging.handlers
import socket

#destination for the XML File
path = '/var/www/html/xml/feucht.xml'
#set up logging
logFormatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
rootLogger = logging.getLogger()
fileHandler = logging.handlers.RotatingFileHandler('/var/log/dht/dht.log',maxBytes=1000000,backupCount=5)
fileHandler.setFormatter(logFormatter)
console = logging.StreamHandler()
rootLogger.addHandler(fileHandler)
rootLogger.addHandler(console)
rootLogger.setLevel(logging.INFO)


#DHT11 Inputs setzen
dht11 = list()
with open('/home/pi/pinconfig/dht11.cfg', mode= 'r') as file:
	for line in file:
		dht11 = line.split(',')
		logging.info("DHT11 GPIOS are: " + str(dht11))

#DHT22 Inputs setzen
dht22 = list()
with open('/home/pi/pinconfig/dht22.cfg', mode= 'r') as file:
	for line in file:
		dht22 = line.split(',')
		logging.info("DHT22 GPIOS are: " + str(dht22))

#find out local ip address (we want to tell the recievers the name of the system)
local = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]

#header - figure out system name
sql = "select name from messsystem where ip = '%s';" % (local)
try:
	db = pymysql.connect(host='localhost', user='webuser', password='t5sLhtva6Ev8xjptFpGhu2zupsy64sgTndg',db='serverraum_temperaturueberwachung',autocommit=True)
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

dhtprefix = systemname.split(' ')[1] + systemname.split(' ')[2]

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
			sql = "insert into messung (zeit , fk_sensorID, temp, feucht) values"
			out = '<?xml version="1.0" encoding="ISO-8859-1" ?><?xml-stylesheet type="text/xsl" href="./actualfeucht.xsl"?><monitoring>'
			now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			logging.debug("beginning")
			#save measurements to the database and produce xml, missing sensors will be created automatically
			for pin in dht11:
				pin = int(pin)
				logging.debug("reading GPIO: " + str(pin))
				sk = 'dht'+ str(dhtprefix) + str(pin)
				try:
					feucht, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)
					sql = sql + " ('%s',func_getSID('%s'), %d, %d)," % (now, sk, temp, feucht)
					for sensor in sensoren:
						if str(sensor[0]) == sk:
							logging.debug("here")
							out= out + '<sensor name = "'+str(sensor[2])+'"><id>'+str(sensor[1])+'</id><temp>'+str(temp)+'</temp><feucht>'+str(feucht)+'</feucht><zeit>'+now+'</zeit></sensor>'
				except Exception as e:
					logging.error(e)
			for pin in dht22:
				pin = int(pin)
				logging.debug("reading GPIO: " + str(pin))
				sk = 'dht'+ str(dhtprefix) + str(pin)
				try:
					feucht, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, pin)
					sql = sql + " ('%s',func_getSID('%s'), %d, %d)," % (now, sk, temp, feucht)
					for sensor in sensoren:
						if str(sensor[0]) == sk:
							logging.debug("here")
							out= out + '<sensor name = "'+str(sensor[2])+'"><id>'+str(sensor[1])+'</id><temp>'+str(temp)+'</temp><feucht>'+str(feucht)+'</feucht><zeit>'+now+'</zeit></sensor>'
				except Exception as e:
					logging.error(e)
			out = out + "</monitoring>"
			logging.debug(out)
			with open(path, "w") as xml:
				xml.write(out)
			logging.info("XML File sucessfully generated")
			logging.debug(sql[:-1] + ";")
			cursor.execute(sql[:-1] + ";")
			logging.info("Data sucessfully inserted into database")
			#wait for 60 seconds
			time.sleep(5)
		except Exception as g:
			logging.error(g)
			logging.info("Database Connection will be reopened")
			db.close()
			break