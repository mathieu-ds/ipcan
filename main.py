# import os
import re      # regex
import json    # json managment
import time;   # get current date
import http.server
import scapy.all as scapy
import webbrowser
import os

class IPScan:
   def __init__(self, ip='192.168.1.1', min=1, max=254):
      self.ip = ip + '/24'
      self.min = min
      self.max = max

   def Process (self):
      self.CreateDefaultJson()
      ipl = self.Arp()
      ipfl = self.IPFilter(ipl)
      datalist = self.ConstructDataList(ipfl)
      self.UpdateJsonFile(datalist)

   def Arp(self):
      ip_list = []
      answered, unanswered = scapy.srp(scapy.Ether(dst="ff:ff:ff:ff:ff:ff")/scapy.ARP(pdst=self.ip),timeout=2)
      for i in answered:
         ip_list.append(i[1].psrc)
      return ip_list

   def IPFilter(self, ip_list):
      # regex : ^192\.168\.1\.1[7-9]\d$ for 170-199
      filtered_ip_list = []
      for ip in ip_list:
         # match = re.search('^192\.168\.1\.1[7-9]\d$', ip)
         match = re.search('^192\.168\.1\.[0-9]\d$', ip)
         if match is not None:
            filtered_ip_list.append(match.group(0))
      return filtered_ip_list

   def ConstructDataList (self, ip_list):
      data_list = []
      for ip in ip_list:
         data = {}
         data["ip"] = ip
         data["status"] = "not available"
         data["date"] = time.strftime('%Y-%m-%d %H:%M')
         data_list.append(data)
      return data_list

   def CreateDefaultJson (self):
      if not os.path.isfile('./ip.json'):
         data_list = []
         for ip in range (self.min, self.max+1):
            data = {}
            data["ip"] = "192.168.1." + str(ip)
            data["status"] = "available"
            data["date"] = "-"
            data_list.append(data)
         self.DataToJsonFile(data_list)

   def ReadJsonData(self):
      with open('ip.json', 'r') as f:
         return json.loads(f.read())

   def UpdateJsonFile(self, data_fromscan):
      data_fromjson = self.ReadJsonData()
      for data in data_fromscan:
         if data is not None:
            index = next((i for i, item in enumerate(data_fromjson) if item["ip"] == data["ip"]), None)
            data_fromjson[index]["status"] = data["status"]
            data_fromjson[index]["date"] = data["date"]
      self.DataToJsonFile(data_fromjson)

   def DataToJsonFile(self, data_list):
      jsonobj = json.dumps(data_list, indent=2)
      with open('ip.json', 'w') as f:
         f.write(jsonobj)

class HttpServer:
   def __init__(self, port, autorun=False):
      self.port = port
      if (autorun == True):
         server_address = ("", self.port)
         server = http.server.HTTPServer
         handler = http.server.CGIHTTPRequestHandler
         # handler.cgi_directories = ["/"]
         print("Serveur actif sur le port :", self.port)
         httpd = server(server_address, handler)
         httpd.serve_forever()

   def RunForever (self):
      server_address = ("", self.port)
      server = http.server.HTTPServer
      handler = http.server.CGIHTTPRequestHandler
      # handler.cgi_directories = ["/"]
      print("Serveur actif sur le port :", self.port)
      httpd = server(server_address, handler)
      httpd.serve_forever()

#############################################################

a = IPScan()
b = IPScan('192.168.0.2', 170, 199)
print(f'a : {a.ip} {a.min} {a.max}')
print(f'b : {b.ip} {b.min} {b.max}')

# ipl = a.Arp()
# ipfl = a.IPFilter(ipl)
a.Process()

# url = 'http://127.0.0.1:8888/ip.html'
# webbrowser.open(url)
HttpServer(8888, True)
