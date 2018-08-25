#!/bin/bash

#set (default) policy

iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP
ip6tables -P INPUT DROP
ip6tables -P FORWARD DROP
ip6tables -P OUTPUT DROP



#flush all chains

iptables -F
iptables -t nat -F
iptables -X
ip6tables -F
ip6tables -X


#add rules

iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

iptables -A INPUT -s 127.0.0.1 -j ACCEPT
iptables -A OUTPUT -d 127.0.0.1 -j ACCEPT

iptables -A INPUT -p tcp -m multiport --dports 22,80,443,3306 -m state --state NEW -j ACCEPT
iptables -A OUTPUT -s 10.0.0.161 -m state --state NEW -j ACCEPT
