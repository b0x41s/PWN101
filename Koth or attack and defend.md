
Add IP and hostname to /etc/hosts
#### ssh bruteforce:  
`hydra -l b0x41s -P /home/b0x41s/hashcat/rockyou.txt 10.0.0.1 ssh -t 4 -v`
#### users:  
`cat /etc/passwd | grep /bin | grep sh`
#### network:   
`ss -tlp `   

`ss -tulp`

`ss -tln`  numeric   

`lsof -i -P -n | grep LISTEN`
#### processes / services:  
`ps aux --forest`

`service --status-all`
#### files
`chown user:group /path/to/file`

`find /path/to/search -name "filename"`  

`find / -perm -4000 -type f 2>/dev/null`
#### misc

`ps aux | grep process_name | grep -v grep | awk '{print $2}' | xargs kill -9`
#### iptables
block ip
`sudo iptables -A INPUT -s 192.168.1.100 -j DROP`
