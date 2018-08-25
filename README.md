# serverroommonitoring
A software built to easily monitor one or more serverooms


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

9) enjoy & feel free to change the passwords                                 