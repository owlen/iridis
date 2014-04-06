#!/usr/bin/python3
import xmlrpc.client
msgserver = xmlrpc.client.ServerProxy('http://127.0.0.1:6712')
print("Connected to message server with functions: %s" % (', '.join(msgserver.system.listMethods())))

#colorserver = xmlrpc.client.ServerProxy('http://127.0.0.1:6711')
#print(colorserver.getvoutcolor('1'))
#print(colorserver.system.listMethods())

def makefilter(offeredInputs, quantityOffered, requestedAsset, Price, kyc, commitment):
    return {
        'offeredInputs': input('space separated list of [txhash:index] entries: '),
        'quantityOffered': input('quantity offered: '),
        'requestedAsset': input('requested asset: '),
        'price': input('price: '),
        'kyc': input('kyc: '),
        'commitment': ''
    }

try:
    while True:
        cmd = input("\nType command ([S]end, [R]eceive, [Q]uit)\n")
        if 'q' == cmd.lower(): break
        if 's' == cmd.lower():
            print(msgserver.send(input('subject: '), input('message: ')))
            continue
        if 'r' == cmd.lower():
            print(msgserver.receive())
            continue
except KeyboardInterrupt:
    from sys import exit
    exit(0)
