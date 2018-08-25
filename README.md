# serverroommonitoring
A software built to easily monitor one or more serverooms

(If you wish to change the passwords: 
		all .py files, connect.php, messages.php and notifications.php include the password, also you have to change the password of the MySQL User

German:

Halten sie folgende Files bereit:
	- ssh keys + authorized keys - /home/pi/.ssh/
	- pinconfigs - /home/pi/
	- interfaces - /etc/network/
	- install.sh - /home/pi/

1) Flashen der SD Karte
	Zum Flashen der SD Karte downloaden Sie die neueste Raspian-lite img und verwenden dann entweder:
		Win32DiskImager
		Etcher
	um das Image zu flashen (Das flashen benötigt einige Zeit

2) Kopieren sie nun die vorher bereitgehaltenen Files (außer die pinconfigs) in die dafür vorgesehenen Ordner

3) In der boot Partition legen sie nun mit dem toch Befehl die Files ssh an
	touch ssh

4) Legen sie nun die SD Karte ein stecken alle GPIO Leitungen an ihren Platz, schließen das Gehäuse und stecken
Sie die Stromversorgung an

5) Verbinden sie sich nun per ssh mit pi:raspberry und ändern anschließend das Passwort für diesen User

6) Rufen Sie die raspi-config auf
	- expanden Sie das Filesystem
	- setzen Sie den Hostnamen
	
7) Stellen Sie sicher, dass ihr System über Internetkonnektivität verfügt

8) Nach dem Reboot starten Sie die install.sh

9) viel Spaß bei der Verwendung  

English:

Prepare the following Files:
	- ssh keys + authorized keys - /home/pi/.ssh/
	- pinconfigs - /home/pi/
	- interfaces - /etc/network/
	- install.sh - /home/pi/

1) Flashing of the SD Card
	To Flash the SD Card simply download the nweste Raspian-lite image and use:
		Win32DiskImager
		Etcher
	to flash the image (flashing the image takes plenty of time)

2) Copy the prepared Files (except the pinconfigs) in the directories they are destined for

3) In the boot partition you have to create a file to enable ssh
	touch ssh

4) Insert the SD, connect all GPIOs and connect the power supply

5) Connect via ssh using pi:raspberry and change the password

6) Issue raspi-config 
	- expanden the Filesystem
	- set the Hostname
	
7) Go for sure that the Raspi has Internetconnectivity

8) After rebooting start the install.sh

9) enjoy                                     