
### Allow all outgoing traffic
sudo iptables -A OUTPUT -j ACCEPT

### Allow incoming traffic related to established connections
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

### Drop all other incoming traffic
sudo iptables -A INPUT -j DROP

