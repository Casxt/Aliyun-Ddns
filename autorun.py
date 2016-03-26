from ddns import Ddns
from autologin import autologin
import time
import datetime
ipv4_domain = "you.ipv4"
ipv6_domain = "you.ipv6"
result = Ddns.check_dns(ipv4_domain,ipv6_domain)
with open(r'Ddns.log', 'a+') as f:
    now = datetime.datetime.utcnow()
    otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
    f.write("#=============================================="+"\n")
    f.write("time:"+otherStyleTime+"\n")
    f.write("login:"+str(login)+"\n")
    f.write("result:"+str(result)+"\n")