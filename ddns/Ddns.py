#!/usr/local/bin/python3
try:
    from ddns import AliyunApi
except:
    import AliyunApi
from pprint import pprint
import json
import time
import datetime
# userdict={
# "DomainName":"casxt.com",
# "RRKeyWord":"test"}
URL = 'http://dns.aliyuncs.com/?'
###########################查询dns记录###########################
def get_dns_recoder(RRKeyWord,DomainName):
    userdict={
    "Action":"DescribeDomainRecords",
    "DomainName":DomainName,
    "RRKeyWord":RRKeyWord}
    recoder = AliyunApi.get_result(userdict)
    recoder_dict = json.loads(recoder)
    return(recoder_dict)
#pprint (get_dns_recoder("casxt.com","test"))
# {'DomainRecords': {'Record': [{'DomainName': 'casxt.com',
#                                'Line': 'default',
#                                'Locked': False,
#                                'RR': 'test',
#                                'RecordId': '77226376',
#                                'Status': 'ENABLE',
#                                'TTL': 600,
#                                'Type': 'A',
#                                'Value': '1.1.1.1'}]},
#  'PageNumber': 1,
#  'PageSize': 1,
#  'RequestId': 'FD8792A0-A432-4181-B477-CA4EBE7B9A89',
#  'TotalCount': 1}
###########################获取RecordId,并修改记录###########################
def change_dns_recoder(recoder_dict,ip):
    userdict={
    "Action":"UpdateDomainRecord",
    "RecordId":recoder_dict['DomainRecords']['Record'][0]['RecordId'],
    "RR":recoder_dict['DomainRecords']['Record'][0]['RR'],
    "Type":recoder_dict['DomainRecords']['Record'][0]['Type'],
    "Value":ip}
    recoder = AliyunApi.get_result(userdict)
    dict = json.loads(recoder)
    return(dict)
###########################获取ip###########################
# 使用ifconfig wlan0命令实现
def get_ip_address(ethname="wlan0"):
    import subprocess
    import re
    (status, output) = subprocess.getstatusoutput('ifconfig %s'%(ethname))
    output = str(output)
    ipv6_rule = r"inet6\saddr\:\s(\w*?:\w*?:\w*?:\w*?:\w*?:\w*?:\w*?:\w*?)/\w*?\sScope\:Global"
    ipv4_rule = r"inet\saddr\:(\w{0,3}.\w{0,3}.\w{0,3}.\w{0,3})\s*Bcast"
    try:
        ipv6_address = re.findall(ipv6_rule,output)[0]
    except:
        ipv6_address = None
    try:
        ipv4_address = re.findall(ipv4_rule,output)[0]
    except:
        ipv4_address = None
    dict = {"ipv4":ipv4_address,"ipv6":ipv6_address}
    return(dict)
def store_ip(): 
    with open(r'Ddns.ip', 'w') as f:
        f.write(dict)
        f.write(dict)
def get_domain_ip(domain):
    import socket
    myaddr = socket.getaddrinfo(domain,'http')[0][4][0]
    return(myaddr)
###########################主程序###########################
# 检查ip与域名记录值是否相同，不同则更改，并记录log
def check_dns(ipv4_domain,ipv6_domain):#主域名用@.domain.XXX表示
    ip = get_ip_address()
    ####ipv4部分####
    ipv4_RRKeyWord = ipv4_domain.split(".",1)[0]
    ipv4_DomainName = ipv4_domain.split(".",1)[1]
    dns4 = get_dns_recoder(ipv4_RRKeyWord,ipv4_DomainName)
    if ip["ipv4"] == dns4['DomainRecords']['Record'][0]['Value']:
        result4 = "Needn't change"
    else:
        try:
            result4 = change_dns_recoder(dns4,ip["ipv4"])
        except:
            result4 = "ipv4 change faild"
    ####ipv6部分####
    ipv6_RRKeyWord = ipv6_domain.split(".",1)[0]
    ipv6_DomainName = ipv6_domain.split(".",1)[1]
    dns6 = get_dns_recoder(ipv6_RRKeyWord,ipv6_DomainName)
    if ip["ipv6"] == dns6['DomainRecords']['Record'][0]['Value']:
        result6 = "Needn't change"
    else:
        try:
            result6 = change_dns_recoder(dns6,ip["ipv6"])
        except:
            result6 = "ipv6 change faild"
    ####log####
    with open(r'Ddns.ip', 'a+') as f:
        now = datetime.datetime.utcnow()
        otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")#2015-01-09T12:00:00Z
        f.write("#=============================================="+"\n")
        f.write("time:"+otherStyleTime+"\n")
        f.write("ip"+str(ip)+"\n")
        f.write("ipv4result"+str(result4)+"\n")
        f.write("ipv6result"+str(result6)+"\n")
    ####返回输出####
    if result4=="Needn't change" and result6=="Needn't change":
        result = "Needn't change"
    elif result4=="Needn't change" and result6!="Needn't change":
        result = "result6 changed"
    elif result6=="Needn't change" and result4!="Needn't change":
        result = "result4 changed"
    elif result6!="Needn't change" and result4!="Needn't change":
        result = "all result changed"
    else:
        result = "check_dns has a error"
    return (result)
# recoder = get_dns_recoder("pi6","casxt.com")
# print (recoder)
# ip = get_ip_address()
# ip = ip["ipv6"]
# print (ip)
# print(change_dns_recoder(recoder,ip))