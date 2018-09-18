#! /bin/bash

sudo apt-get install apache2 -y
sudo apt-get install pure-ftpd -y
sudo apt-get install xinetd telnetd -y
sudo apt-get install dillo -y
sudo apt-get install nmap -y
sudo apt-get install ettercap-graphical -y
sudo apt-get install maradns -y
sudo apt-get install maradns-deadwood -y
sudo apt-get install hping3 -y
sudo apt-get install udhcpd -y
sudo apt-get install udhcpc -y
sudo apt-get install dnsmasq -y
sudo apt-get install curl -y
sudo apt-get install distcc -y
sudo apt-get install chromium-browser -y
sudo apt-get install ipsec-tools -y
sudo apt-get install strongswan -y
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && chmod a+rwx msfinstall && ./msfinstall
