#!/bin/sh
set -e

echo "[dmz] installing tools..."
apk add --no-cache iptables socat > /dev/null

# Basic policy: accept on loopback, drop forwarding by default
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
iptables -P FORWARD DROP

# Allow established
iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT

# Proxy services from DMZ -> OT using socat (listening on DMZ iface)
# Map ports so that IT side can only reach these gateways:
#  - 18080 -> HMI:80 (Level 3)
#  - 1840  -> OPCUA:4840 (Level 2)
#  - 1502  -> Conpot:502 (Level 1)
echo "[dmz] starting socat proxies..."
socat TCP-LISTEN:18080,fork,reuseaddr TCP:hmi:80 &
socat TCP-LISTEN:1840,fork,reuseaddr  TCP:opcua:4840 &
socat TCP-LISTEN:1502,fork,reuseaddr  TCP:conpot:502 &

# Allow DMZ ingress to the proxy ports from orchestration_net
# (Docker isolates bridges; since this container joins both dmz_net and lower nets,
# traffic reaches these listeners on the dmz interface.)
iptables -A INPUT -p tcp --dport 18080 -j ACCEPT
iptables -A INPUT -p tcp --dport 1840  -j ACCEPT
iptables -A INPUT -p tcp --dport 1502  -j ACCEPT

# Drop anything else destined to lower networks (simulated)
iptables -A FORWARD -j DROP

echo "[dmz] ready. tailing..."
tail -f /dev/null
