#!/bin/bash
#set default policy
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
#flush all chains
iptables -F
iptables -t nat -F
iptables -X
