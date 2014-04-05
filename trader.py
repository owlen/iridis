#!/usr/bin/python3
import xmlrpc.client
msgserver = xmlrpc.client.ServerProxy('http://127.0.0.1:6712')
print("Connected to message server with functions: %s" % (', '.join(msgserver.system.listMethods())))

#colorserver = xmlrpc.client.ServerProxy('http://127.0.0.1:6711')
#print(colorserver.getvoutcolor('1'))
#print(colorserver.system.listMethods())

try:
    while True:
        cmd = input("\nType command ([P]ropose, [O]ffer, [I]nbox, [Q]uit)\n")
        if 'q' == cmd.lower(): break
        if 'i' == cmd.lower():
            print(msgserver.listen(''))
            continue
        if 'o' == cmd.lower():
            print(msgserver.offer(input("\noffer\n")))
            continue
        if 'p' == cmd.lower():
            print(msgserver.propose(input("\npropose\n")))
            continue
except KeyboardInterrupt:
    from sys import exit
    exit(0)
