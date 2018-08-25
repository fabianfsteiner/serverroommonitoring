# -*- coding: utf-8 -*-
import pymysql
import logging
import logging.handlers
import datetime
import os
import time
import sys
import socket

def save_to_messages_db(cur, nowf, type, title, sms):
	"""
	Saves outgoing messages to the messages db
	:param cur: the cursor on serverraum_temperaturueberwachung
	:param nowf: the actual time formatted
	:param type: the type of the sms
	:param title: the title of the sms
	:param sms: the sms text
	"""
	try:
		cur.execute('select ip from messsystem;')
		systeme = cur.fetchall()
		for system in systeme:
			logging.info("Saving sms in: " +system[0])
			mdb = pymysql.connect(host=system[0], user='webuser', password='t5sLhtva6Ev8xjptFpGhu2zupsy64sgTndg',db='messages',autocommit=True)
			mcursor = mdb.cursor()
			sql = "insert into message values ('%s', %d, '%s', '%s')" % (str(nowf),type,title, sms)
			logging.debug(sql)
			mcursor.execute(sql)
			mdb.close()
	except Exception as e:
		logging.error(e)

max_temp = 35.0;
max_hum = 70.0;
interval = 30
max_rauch = 10
silent = False

#set up logging
logFormatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
rootLogger = logging.getLogger()
fileHandler = logging.handlers.RotatingFileHandler('/var/log/smsd/smsd.log',maxBytes=1000000,backupCount=5)
fileHandler.setFormatter(logFormatter)
console = logging.StreamHandler()
rootLogger.addHandler(fileHandler)
rootLogger.addHandler(console)
rootLogger.setLevel(logging.INFO)

#reviever add recievers in /etc/smsd/recievers.list
To = ""
try:
	with open("/etc/smsd/recievers.list", mode='r') as recievers:
		for reciever in recievers:
			logging.info("Adding reciever: " + reciever)
			To = To + "To: " + reciever + "\n"
except Exception as tel:
	logging.error(tel)
	sys.exit()
#general path
path = "/var/spool/sms"
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
up = To + "\nTemperaturüberwachung "+systemname+":\n"

while True:
	with open("/etc/smsd/sms.conf") as f:
		logging.info("Loaded configuration:")
		for line in f:
			key = line.split(':')[0]
			value = line.split(':')[1].strip()
			if key == "interval":
				interval = int(value)
				logging.info("interval: " + str(interval))
			if key == "silent":
				silent = bool(value)
				logging.info("muted: " + str(silent))
			if key == "max_temp":
				max_temp = float(value)
				logging.info("max_temp: " + str(max_temp))
			if key == "max_hum":
				max_hum = float(value)
				logging.info("max_hum: " + str(max_hum))
			if key == "max_smoke":
				max_rauch = value
				logging.info("max_smoke: " + str(max_rauch))
	try:
		while True:
			now = datetime.datetime.now()
			nowf = now.strftime("%Y-%m-%d %H:%M:%S")
			past = (now - datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
			past30 = now - datetime.timedelta(minutes=interval)
			past18 = now - datetime.timedelta(hours=18)
			tm = now + datetime.timedelta(days=1)
			yes = (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
			if silent and not datetime.datetime.fromtimestamp(os.stat("/home/pi/alive.txt").st_mtime) < past18:
				time.sleep(10)
				logging.info("muted")
				continue
			sms = up
			title = ""
			logging.info("try connecting to db")
			try:
				connection = pymysql.connect(host='localhost', user='webuser', password='t5sLhtva6Ev8xjptFpGhu2zupsy64sgTndg',db='serverraum_temperaturueberwachung',autocommit=True)
			except Exception as e:
				logging.error(e)
				continue
			cur = connection.cursor()
			if datetime.datetime.fromtimestamp(os.stat("/home/pi/alive.txt").st_mtime) < past18:
				cur.execute("select avg(temp) as temp , avg(feucht) as feucht,  avg(wasser) as wasser , avg(rauch) as rauch, sensorPosition from view_24 where zeit > '"+yes+"' group by sensorPosition;")
				results = cur.fetchall()
				da = up + "Das System ist online.\nDurschnittswerte:\n"
				with open("/var/spool/sms/outgoing/alive.txt", mode='w') as f:
					print(up + "Das System ist online.\nDurschnittswerte:\n", file=f)
					for result in results:
						if result[0] == None and result[1] == None and result[2] == None:
							print(result[4] + ": " + str(result[3]) + "\n", file=f)
							da = da + result[4] + ": " + str(result[3]) + "\n"
						elif result[0] == None and result[1] == None:
							print(result[4] + ": " + str(result[2]) + "\n", file=f)
							da = da + result[4] + ": " + str(result[2]) + "\n"
						elif result[1] == None:
							print(result[4] + ": " + str(result[0]) + "°C\n", file=f)
							da = da + result[4] + ": " + str(result[0]) + "°C\n"
						else:
							print(result[4] + ": " + str(result[0]) + "°C / " + str(result[1]) +" %\n", file=f)
							da = da + result[4] + ": " + str(result[0]) + "°C / " + str(result[1]) +" %\n"
				os.system("touch -d "+tm.strftime("%Y%m%d")+" /home/pi/alive.txt")
				save_to_messages_db(cur, nowf, 2, "alive", da)
				logging.info("daily SMS sent")
				cur.execute("delete from messung where zeit < '"+yes+"';")
				logging.info("daily delete")
				connection.close()
				continue
			if not len(os.listdir(path + '/checked/')) == 0:
				continue
			cur.execute("select avg(temp) as temp , avg(feucht) as feucht,  avg(wasser) as wasser , avg(rauch) as rauch, sensorName from web where zeit > '"+past+"' group by sensorName;")
			results = cur.fetchall()
			msgs = dict()
			for result in results:
				try:
					if result[0] == None and result[1] == None and result[2] == None:
						if float(result[3]) > max_rauch:
							msgs[result[4] + "r"] = "Die Werte an Sensor " + result[4] + " sind außerhalb des Normalbereichs: " + str(result[3]) + "\n"
						continue
					elif result[0] == None and result[1] == None:
						if float(result[2]) > 0:
							msgs[result[4] + "w"] = "Die Werte an Sensor " + result[4] + " sind außerhalb des Normalbereichs: " + str(result[2]) + "\n"
						continue
					elif result[1] == None:
						if float(result[0]) > max_temp:
							msgs[result[4] + "t"] = "Die Werte an Sensor " + result[4] + " sind außerhalb des Normalbereichs: " + str(result[0]) + "°C\n"
						continue
					else:
						if float(result[0]) > max_temp and float(result[1]) > max_hum:
							msgs[result[4] + "tf"] = "Die Werte an Sensor " + result[4] + " sind außerhalb des Normalbereichs: " + str(result[0]) + "°C/" + str(result[1]) + "%\n"
						continue
				except Exception as e:
					logging.error(e)
			files = os.listdir(path+"/sent/")
			for name, message in msgs.items():
				for file in files:
					for n in str(file)[:-4].split("-"):
						if name == n and (datetime.datetime.fromtimestamp(os.stat(path+"/sent/"+str(file)).st_mtime) > past30):
							logging.info("")
							message = ""
							name = ""
				sms += message
				if message != "":
					title += name + "-"
				logging.info("added " + message + "to SMS")
			if not title == "":
				logging.info("title of sms is: "+ title)
				save_to_messages_db(cur, nowf, 1, title[:-1], sms)
				with open("/var/spool/sms/outgoing/"+title[:-1]+".txt", mode='w') as f:
					print(sms, file=f)
			connection.close()
			time.sleep(30)
	except Exception as outer:
		logging.error(outer)
		connection.close()