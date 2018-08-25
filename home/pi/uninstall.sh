mysql -e "drop database messages"
mysql -e "drop database serverraum_temperaturueberwachung"
apt purge -y apache2 mysql-server php php-mysql php-xml smstools python3-pip python3-pymysql git firewalld
rm -rf /var/log/smsd
rm -rf /var/log/1wire
systemctl disable 1wire
systemctl disable water
systemctl disable smsd
systemctl disable failover
systemctl disable respond
systemctl stop 1wire
systemctl stop smsd
systemctl stop failover
systemctl stop respond
systemctl stop water
rm -rf /var/www/html/*
rm -rf /home/pi/skripts
rm -rf /etc/smsd
rm -rf /home/pi/incoming
rm /home/pi/uninstall.sh
rm /home/pi/install.sh /install.sh
rm /lib/systemd/system/1wire.service
rm /lib/systemd/system/water.service
rm /lib/systemd/system/failover.service
rm /lib/systemd/system/respond.service
rm /lib/systemd/system/smsd.service