apt update && apt upgrade -y && apt install -y apache2 mysql-server php php-mysql php-xml smstools python3-pip python3-pymysql git firewalld python3-rpi.gpio build-essential libusb-dev python-dev python-openssl python-pymysql
systemctl enable firewalld
systemctl start firewalld
cd /
git init
git remote add origin git@github.com:fabianfsteiner/serverroommonitoring.git
git pull origin master
mv /etc/usb_modeswitch.d/12d1 /etc/usb_modeswitch.d/12d1:1f01
mkdir /var/log/smsd/
mkdir /var/log/1wire
mkdir /var/log/water
mkdir /var/log/pullup
mkdir /var/log/dht
mkdir /home/pi/incoming
mkdir /home/pi/lib
cd /home/pi/lib
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
sudo python setup.py install
cd /
touch /home/pi/alive.txt
chown pi:pi -R /home/pi/incoming
sed -i "/bind-address.*=.*/c\bind-address            = 0.0.0.0" /etc/mysql/mariadb.conf.d/50-server.cnf
systemctl restart mysql
mysql -e "source creates.sql"
systemctl enable 1wire
systemctl enable water
systemctl enable dht
systemctl enable smsd
systemctl enable failover
systemctl enable respond
systemctl start 1wire
systemctl start water
systemctl start dht
systemctl start smsd
systemctl start failover
systemctl start respond
echo -n "Provide PIN: "
read answer
sed -i "/device = .*/c\device = /dev/ttyUSB0" /etc/smsd.conf
sed -i "/pin = .*/c\pin = $answer" /etc/smsd.conf
systemctl restart smstools
rm creates.sql
rm install.sh
rm -rf .git
echo "# activating 1-wire\n" >> /boot/config.txt
echo "dtoverlay=w1-gpio" >> /boot/config.txt
firewall-cmd --permanent --add-service=ssh
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
firewall-cmd --permanent --add-service=mysql
firewall-cmd --reload
echo -n "A reboot is required to apply the configuration. Reboot? (y/n)? "
read reb
if echo "$reb" | grep -iq "^y" ;then
    echo "Goodbye"
    systemctl reboot
else
    echo "Please reboot the system when convenient."
fi
echo "Goodbye."