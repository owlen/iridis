#!/usr/bin/python3

# Connect to bitmessage XML-RPC server running with the given keys.dat on port
# 6713 and expose send and receive functions

# Make sure the port is available
port = 6713
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if 0 == sock.connect_ex(('localhost', port)):
    sock.close()
    raise Exception("port %d is in use, aborting" % (port,))

# Run bitmessage
from subprocess import Popen, DEVNULL
from os import path
curpath = path.dirname(path.abspath(__file__))
# bitmessageprocess = Popen(('python', curpath + '/PyBitmessage/src/bitmessagemain.py'), stdout=DEVNULL)
bitmessageprocess = Popen('C:\\Dudu\\CC\\BitMessage\\Bitmessage.exe')

# Connect to its XML-RPC server
import xmlrpc.client
bitmessage = xmlrpc.client.ServerProxy("http://admin:123@127.0.0.1:%d" % (port,))

# Implement required functionality

# UTF-8 to base64 and back
from base64 import b64encode, b64decode
def b64enc(s): return b64encode(bytes(s, 'utf-8')).decode('utf-8')
def b64dec(b): return b64decode(b).decode('utf-8')

# Send message to chan
from json import dumps as jsdumps
# FIXME This, obviously, should not be hardcoded.
toaddress = '2cUEpXgRYZAmVqqWd8tzAFLr8UXtCbZy4g'
fromaddress = '2cW9hFSVrVs2AcqwKgkcx6QtL6fgXNa4AP'
def send(subject, body):
    if not type(body) is str: body = jsdumps(body)
    subject, body = map(b64enc, (subject, body))
    return bitmessage.sendMessage(toaddress, fromaddress, subject, body)

# Get a list of all new messages
from json import loads as jsloads
def receive():
    messages = []
    inbox = jsloads(bitmessage.getAllInboxMessages())['inboxMessages']
    for msgid in (m['msgid'] for m in inbox):
        message = jsloads(bitmessage.getInboxMessageByID(msgid))['inboxMessage'][0]
        if 'BM-' + toaddress == message['toAddress']:
            fromaddress = message['fromAddress']
            subject, body = map(b64dec, (message['subject'], message['message']))
            try: body = jsloads(body)
            except ValueError: pass
            messages.append({'subject': subject, 'body': body, 'fromaddress': fromaddress})
        bitmessage.trashMessage(msgid)
    if len(messages) > 0: print('transfered incoming messages: ', messages)
    return messages

def close():
    bitmessageprocess.terminate()

if __name__ == '__main__':
    wallet = {
        'obc:1737d32b3bfdd06a177435a00e4ddd8befe804daece3cfa19508f1ec7a2df2a9:0:241614': 'red',
        'obc:f9931ace552776defae1114f551cfb09a6453f13956e042e8d78a8fd42af804b:0:241616': 'blue',
        'obc:b2e2fe91385b66b413d23d00c45d2958c273ba6248c2a5da0d3738ccffef74e9:0:242505': 'GLD',
        'obc:ebf6742cd705bfd3dbfb6470dadbf248a6cf90f4b54775ad54ce79ed45bd6365:0:242505': 'SLV'
    }
    try:
        while True:
            subject = input('subject: ')
            if 'proposal' == subject:
                give = {}
                give['colordef'] = input('give colordef: ')
                give['quantity'] = input('give quantity: ')
                give['utxos'] = []
                for i in range(int(input('how many utxos: '))):
                    txid = input('txid: ')
                    vout = input('vout: ')
                    scriptPubKey = input('scriptPubKey: ')
                    give['utxos'].append({'txid': txid, 'vout': vout, 'scriptPubKey': scriptPubKey})
                take = {}
                take['colordef'] = input('take colordef: ')
                take['quantity'] = input('take quantity: ')
                take['address'] = input('take address: ')
                body = {'scheme': -1, 'version': -1, 'take': take, 'give': give, 'proposalid': input('proposal hash: ')}
            else: body = input('free text for message body: ')
            if 'y' == input('send this message? (y/n) '): print(send(subject, body))
    except KeyboardInterrupt:
        close()
        from sys import exit
        exit(0)
