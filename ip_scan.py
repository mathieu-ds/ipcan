#! /usr/bin/python3
import os
import re
import json
import time;
# print(os.sys.path)
os.sys.path.append("/home/lumiplan/.local/lib/python3.8/site-packages")
import scapy.all as scapy

def Arp(ip):
    ip_list = []
    arp_r = scapy.ARP(pdst=ip)
    br = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    request = br/arp_r
    answered, unanswered = scapy.srp(request, timeout=1)
    for i in answered:
        ip_list.append(i[1].psrc)

    return ip_list

def IPFilter(min, max, ip_list):
    # regex : ^192\.168\.1\.1[7-9]\d$
    filtered_ip_list = []
    for ip in ip_list:
        match = re.search('^192\.168\.1\.1[7-9]\d$', ip)
        if match is not None:
            filtered_ip_list.append(match.group(0))
    
    return filtered_ip_list

def ToJsonFile(data_list):
    jsonobj = json.dumps(data_list, indent=2)
    with open('ip.json', 'w') as f:
        f.write(jsonobj)

def ConstructDataList (ip_list):
    data_list = []
    for ip in ip_list:
        data = {}
        data["ip"] = ip
        data["status"] = "not available"
        data["date"] = time.strftime('%Y-%m-%d %H:%M')
        data_list.append(data)
    return data_list

def CreateDefaultJson():
    data_list = []
    for ip in range (170, 200):
        data = {}
        data["ip"] = "192.168.1." + str(ip)
        data["status"] = "available"
        data["date"] = "-"
        data_list.append(data)
    ToJsonFile(data_list)

def ReadJsonData():
    with open('ip.json', 'r') as f:
        return json.loads(f.read())

def UpdateJsonFile(data_fromscan):
    data_fromjson = ReadJsonData()
    for data in data_fromscan:
        index = next((i for i, item in enumerate(data_fromjson) if item["ip"] == data["ip"]), None)
        #print (val)
        data_fromjson[index]["status"] = data["status"]
        data_fromjson[index]["date"] = data["date"]

    ToJsonFile(data_fromjson)


#CreateDefaultJson()
#data = ReadJsonData()


raw_ip_list = Arp('192.168.1.1/24') # call the methodsudo
filtered_ip_list = IPFilter(170,199, raw_ip_list)
data_list = ConstructDataList(filtered_ip_list)
UpdateJsonFile(data_list)
