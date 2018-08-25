#!/usr/bin/python
import time, subprocess
import logging
import logging.handlers
import RPi.GPIO as GPIO

#set up logging
logFormatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
rootLogger = logging.getLogger()
fileHandler = logging.handlers.RotatingFileHandler('/var/log/pullup/pullup.log',maxBytes=1000000,backupCount=5)
fileHandler.setFormatter(logFormatter)
console = logging.StreamHandler()
rootLogger.addHandler(fileHandler)
rootLogger.addHandler(console)
rootLogger.setLevel(logging.INFO)

#Pin Modus setzen
GPIO.setmode(GPIO.BCM)

#Inputs setzen
pins = list()
with open('/home/pi/pinconfig/pullup.cfg', mode= 'r') as file:
	for line in file:
		pins = line.split(',')
		logging.info("GPIOS are: " + str(pins))
		for pin in pins:
			GPIO.setup(int(pin), GPIO.OUT)
			GPIO.output(int(pin), GPIO.HIGH)
			logging.info("GPIO pulled up: " + pin )