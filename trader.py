#!/usr/bin/python3
import xmlrpc.client

colorserver = xmlrpc.client.ServerProxy('http://127.0.0.1:6711')
print(colorserver.getvoutcolor('1'))
print(colorserver.system.listMethods())

msgserver = xmlrpc.client.ServerProxy('http://127.0.0.1:6712')
print(msgserver.listen('1'))
print(msgserver.system.listMethods())
