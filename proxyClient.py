#!/bin/python3
import socket
import sys
import http.client
import requests
import os
#from cacheDir import *
class proxyClient():
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    arg = ""
    strHeader = ""
    inCache = 0
    codeStatus = ""
    #slist = []
    #cachedir = cacheDir()
    #def __init__(self, arg1, cache1):
    def __init__(self, arg1):
        self.arg = arg1
        #self.cachedir = cache1
    def getObject(self):
        port = 80
        #request = "GET " + self.arg[27:47] + " HTTP/1.1\nHost: " + self.arg[7:26] + "\nConnection: close\n\n"
        request = "GET " + self.arg[31:47] + " HTTP/1.1\nHost: " + self.arg[7:26] + "\n\n"
        #request = "GET " + self.arg + " HTTP/1.1\n\n"
        #print(request)
        #r = requests.get(url = self.arg, headers={"Accept-Ranges":"none"})
        r = requests.get(url = self.arg)
        #response = requests.get(self.arg, stream=True).headers['Content-length']
        self.makeString(r)
        if r.status_code == 200:
            self.codeStatus = "HTTP/1.1 200 OK"
            self.writeCache(r)
        else:
            self.codeStatus = "HTTP/1.1 " + r.status_code + "Not Found"
        if self.inCache == 0:
            print("---RETURNING OBJECT FROM SERVER---")
            print(self.codeStatus)
            print(r.headers)
            print("\r\n\r\n")
        else:
            print("---RETURNING OBJECT FROM CACHE---")
            print(self.codeStatus)
            print(self.strHeader.replace("|", "\n"))
            print("\r\n\r\n")
        if r.headers['Content-Type'] == 'text/html':
            print(r.text)
        else:
            print("Content is binary")
        #responseAll = bytearray()
        #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #host = socket.gethostname()
        #host = self.arg[7:26]
        #s.bind((host, port))
        #s.connect((host, port))
        #s.sendall(request.encode('utf-8'))
        #s.send(self.arg)
        #s.request("GET", "/")
        #response = s.getresponse()
        #headers = response.getheaders()
        #print(response)
        #print(headers)
        #print(self.arg[7:26])
        #while 1: 
        #    data = s.recv(1024)
        #    if not data: break
        #    responseAll += data
        #s.close()
        #print(r.text)
        #print(repr(data))
        #print(responseAll)
        #print(data)
    def writeCache(self, r):
        slist = []
        #print ("CURRENT " + os.getcwd())
        directory = '/u/css/depaolaat/4450/lab2/cacheDir'
        if not os.path.exists(directory):
            os.makedirs(directory)
        #    os.mknod(directory + '/cacheDir1.txt')
        f = open(directory + "/cacheDir1.txt", "a+")
        with open(directory + '/cacheDir1.txt', "r") as mydata:       
            line = mydata.readline()
            count = 1
            while line:
                slist.append(line)
                print("Line {}: {}".format(count, line.strip()))
                line = mydata.readline()
                count += 1
        print("PLATYPUS")
        print(slist)
        with open(directory + '/cacheDir1.txt', 'a+') as mydata:
            if self.strHeader in slist:
                self.inCache = 1
            else:
                mydata.write(self.strHeader)
                with open(directory + '/cacheDir2.txt', 'ab') as binaryData:
                    binaryData.write(r.content)
    def makeString(self, r):
        self.strHeader = self.arg + "|Last-Modified: " + r.headers['Last-Modified'] + "|Content-Length: " + r.headers['Content-Length'] + "|Content-Type: " + r.headers['Content-Type']
