#-*- coding: utf-8 -*-
#! /usr/bin/env python

# Client and server for udp (datagram) echo.
#
# Usage: udpecho -s [port]            (to start a server)
# or:    udpecho -c host [port] <file (client)

import sys
from socket import *
import SocketServer
from os.path import exists

ECHO_PORT = 50000 + 7
BUFSIZE = 1024

def main():
    if len(sys.argv) < 2:
        usage()
    if sys.argv[1] == '-s':
        server()
    elif sys.argv[1] == '-c':
        client()
    else:
        usage()

def usage():
    sys.stdout = sys.stderr
    print('Usage: udpecho -s [port]            (server)')
    print('or:    udpecho -c host [port] <file (client)')
    sys.exit(2)

def server():
    if len(sys.argv) > 2:
        port = eval(sys.argv[2])
    else:
        port = ECHO_PORT
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('', port))
    print('udp echo server ready')
    data_transferred = 0
    while 1:
        data, addr = s.recvfrom(BUFSIZE)
        img = s.recv(1024)
        print('server received %r from %r' % (data, addr))
        s.sendto(data, addr)
        
        if data == "Photo":
            with open('/home/pi/Documents/Final/' + data + '.jpg', 'wb') as f:
                try:
                    print('asd')
                    while  img:
                        f.write(img)
                        data_transferred += len(img)
                        img = s.recv(1024)
                        print('d')
                except Exception as e:
                    print(e)
 
            print('파일[%s] 전송종료. 전송량 [%d]' %(filename+'.jpg', data_transferred))
            

def client():
    if len(sys.argv) < 3:
        usage()
    host = sys.argv[2]
    if len(sys.argv) > 3:
        port = eval(sys.argv[3])
    else:
        port = ECHO_PORT
    addr = host, port
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('', 0))
    print('udp echo client ready, reading stdin')
    while 1:
        line = sys.stdin.readline()
        if not line:
            break
        s.sendto(line, addr)
        data, fromaddr = s.recvfrom(BUFSIZE)
        print('client received %r from %r' % (data, fromaddr))
        

main()