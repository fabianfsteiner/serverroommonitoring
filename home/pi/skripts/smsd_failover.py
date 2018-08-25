# -*- coding: utf-8 -*-
import logging
import logging.handlers
import datetime
import os
import time
import socket
import pymysql

#find out local ip address (we don't want to forward failed sms packets to our own system)
local = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
#set up logging
logFormatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
rootLogger = logging.getLogger()
fileHandler = logging.handlers.RotatingFileHandler('/var/log/smsd/failover.log',maxBytes=1000000,backupCount=5)
fileHandler.setFormatter(logFormatter)
console = logging.StreamHandler()
rootLogger.addHandler(fileHandler)
rootLogger.addHandler(console)
rootLogger.setLevel(logging.INFO)
#specify paths for failed sms
path = "/var/spool/sms/checked/"
failed = "/var/spool/sms/failed/"
def send(path, file, systeme):
	"""
	Forwards the sms to other systems. Tries every available System until it works
	:param path: dictionary
	:param file: filename
	:param systeme: the systems to try
	"""
	for sys in systeme:
		try:
			if os.system("scp "+ path + str(file) + " pi@"+sys[0]+":incoming") == 0:
				os.system("mv "+ path + str(file) + " /var/spool/sms/sent/")
				logging.info("SMS forwarded to " + sys[1])
				break
		except Exception as s:
			logging.error(s)

while True:
	try:
		db = pymysql.connect(host='localhost', user='webuser', password='La4R2uyME78hAfn9I1pH',db='serverraum_temperaturueberwachung',autocommit=True)
		cursor = db.cursor()
		logging.info("Connected to database")
		sql = "select ip, name from messsystem where ip != '%s';" % (local)
		cursor.execute(sql)
		systeme = cursor.fetchall()
		db.close()
	except Exception as e:
		logging.error(e)
		continue
	try:
		while True:
			now = datetime.datetime.now()
			past = (now - datetime.timedelta(seconds=225))
			files = os.listdir(path)
			for file in files:
				if datetime.datetime.fromtimestamp(os.stat(path+str(file)).st_mtime) < past:
					send(path, file, systeme)
			files = os.listdir(failed)
			for file in files:
				os.system("sed -i \'2i\'"  + failed + str(file))
				os.system("sed -i \'3~5d\' "  + failed + str(file))
				send(failed, file, systeme)
			if len(os.listdir("/home/pi/incoming")) > 0:
				os.system("mv /home/pi/incoming/* /var/spool/sms/outgoing")
				logging.info("moved files to Outgoing")
			time.sleep(10)
	except Exception as outer:
		logging.error(outer)