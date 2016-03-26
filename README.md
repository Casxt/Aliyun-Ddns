# Aliyun-Ddns
Use Aliyun dns as Ddns

Only available for linux(use ifconfig command to get local ip)
you can change the get_ip_address function in ddns/Ddns.py to use other way to get you ip.
require both ipv4 and ipv6 but you can simply delete the ipv6/ipv4 part of check_dns function in ddns/Ddns.py to use the only one mode.

1.fill you AccessKeyId and AccessKeySecret in the ddns/Aliyunapi.py
2.fill you ipv4_domain and ipv6_domain in the autorun.py
3.run autorun.py in corn (you can use time.sleep(300) as well but sometime this will cause something terrible , personally I recommend you to sue corn)
4.it will check whether the ip address has changed and automatically update the dns recoder , and create log naemd Ddns.ip and Ddns.log.
