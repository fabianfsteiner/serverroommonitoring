# -*- coding: utf-8 -*-
import pymysql
import logging
import logging.handlers
import datetime
import os
import time
import re
import sys
import socket


max_temp = 35.0;
max_hum = 70.0;
interval = 30
silent = False
max_rauch = 10

#set up logging
logFormatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
rootLogger = logging.getLogger()
fileHandler = logging.handlers.RotatingFileHandler('/var/log/smsd/smsd_respond.log',maxBytes=1000000,backupCount=5)
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
#text of the help message
help = up + "Available commands: \nHELP - Displays all commands\nSTATUS - Displays actual status\nMUTE and UNMUTE\nINTERVAL: mins - to change the interval\n\
Same Usage:\nMAXTEMP: degrees\nMAXHUM: percent\nMAXSMOKE: int [0; 100]\nnot case sensitive!"

while True:
	with open("/etc/smsd/sms.conf") as f:
		logging.info("reading configuration from sms.conf")
		for line in f:
			key = line.split(':')[0]
			value = line.split(':')[1].strip()
			if key == "interval":
				interval = int(value)
			if key == "silent":
				silent = bool(value)
			if key == "max_temp":
				max_temp = value
			if key == "max_hum":
				max_hum = value
			if key == "max_smoke":
				max_rauch = value
	try:
		while True:
			now = datetime.datetime.now()
			nowf = now.strftime("%Y-%m-%d %H:%M:%S")
			rec = (now - datetime.timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S")
			files = os.listdir(path+"/incoming/")
			changed= False
			try:
				connection = pymysql.connect(host='localhost', user='webuser', password='t5sLhtva6Ev8xjptFpGhu2zupsy64sgTndg',db='serverraum_temperaturueberwachung',autocommit=True)
				cur = connection.cursor()
				cur.execute('select ip from messsystem;')
				systeme = cur.fetchall()
			except Exception as e:
				logging.error(e)
			for file in files:
				logging.info("new sms recieved " + file)
				with open(path + "/incoming/" +file) as f:
					for line in f:
						line = str(line)
						if re.match( r'status', line, re.IGNORECASE):
							logging.info("try connecting to db")
							try:
								#get average temp over the last 15 minutes
								cur.execute("select avg(temp) as temp , avg(feucht) as feucht,  avg(wasser) as wasser , avg(rauch) as rauch, sensorPosition from view_24 where zeit > '"+rec+"' group by sensorPosition;")
								results = cur.fetchall()
								sms = up + "Das System ist online.\nDurschnittswerte:\n"
								with open("/var/spool/sms/outgoing/status.txt", mode='w') as f:
									print(up + "Das System ist online.\nDurschnittswerte:\n", file=f)
									for result in results:
										if result[0] == None and result[1] == None and result[2] == None:
											print(result[4] + ": " + str(result[3]) + "\n", file=f)
											sms = sms + result[4] + ": " + str(result[3]) + "\n"
										elif result[0] == None and result[1] == None:
											print(result[4] + ": " + str(result[2]) + "\n", file=f)
											sms = sms + result[4] + ": " + str(result[2]) + "\n"
										elif result[1] == None:
											print(result[4] + ": " + str(result[0]) + "°C\n", file=f)
											sms = sms + result[4] + ": " + str(result[0]) + "°C\n"
										else:
											print(result[4] + ": " + str(result[0]) + "°C / " + str(result[1]) +" %\n", file=f)
											sms = sms + result[4] + ": " + str(result[0]) + "°C / " + str(result[1]) +" %\n"
								#writing outgoing message to messages db
								for system in systeme:
									logging.info("Saving sms in: " +system[0])
									mdb = pymysql.connect(host=system[0], user='webuser', password='t5sLhtva6Ev8xjptFpGhu2zupsy64sgTndg',db='messages',autocommit=True)
									mcursor = mdb.cursor()
									#sms is type 3 == requested info
									sql = "insert into message values ('%s', %d, '%s', '%s')" % \
									(str(nowf),3,"status", sms)
									mcursor.execute(sql)
									mdb.close()
								logging.info("status SMS sent as requested")
								connection.close()
							except Exception as e:
								logging.error(e)
							continue
						elif re.match( r'mute', line, re.IGNORECASE):
							logging.info("mute was requested")
							silent = True
							changed = True
							continue
						elif re.match( r'unmute', line, re.IGNORECASE):
							logging.info("unmute was requested")
							silent = False
							changed = True
							continue
						elif re.match( r'interval:', line, re.IGNORECASE):
							interval = int(line.split(':')[1].strip())
							logging.info("change of interval to "+str(interval)+" was requested")
							changed = True
							continue
						elif re.match( r'maxtemp:', line, re.IGNORECASE):
							max_temp = float(line.split(':')[1].strip())
							logging.info("changing max temp to "+str(max_temp)+" was requested")
							changed = True
							continue
						elif re.match( r'maxhum:', line, re.IGNORECASE):
							max_hum = float(line.split(':')[1].strip())
							logging.info("changing max hum to "+str(max_hum)+" was requested")
							changed = True
							continue
						elif re.match( r'maxsmoke:', line, re.IGNORECASE):
							max_rauch = float(line.split(':')[1].strip())
							logging.info("changing max smoke to "+str(max_rauch)+" was requested")
							changed = True
							continue
						elif re.match( r'help', line, re.IGNORECASE):
							logging.info("help was requested")
							logging.debug(help)
							with open("/var/spool/sms/outgoing/help.txt", mode="w") as f:
								print(help, file=f)
							continue
				os.system("rm " + path + "/incoming/" + file) 
			if changed:
				if not silent:
					silent = ""
				with open("/etc/smsd/sms.conf", mode="w") as f:
					print("interval: " + str(interval), file=f)
					print("silent: " + str(silent), file=f)
					print("max_temp: " + str(max_temp) , file=f)
					print("max_hum: " + str(max_hum) , file=f)
					print("max_smoke: " + str(max_rauch) , file=f)
				logging.info("New Configuration was saved")
				os.system("systemctl restart smsd")
				logging.info("smsd has successfully loaded the new configuration")
			#wait for 15 seconds
			time.sleep(15)
	except Exception as outer:
		logging.error(outer)