#!/usr/bin/python3
import jsonrpclib
msgserver = jsonrpclib.Server('http://127.0.0.1:6712')
#colorserver = jsonrpclib.Server('http://127.0.0.1:6711')

def makefilter():
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
