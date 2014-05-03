#!/usr/bin/python3

# Connect to bitmessage XML-RPC server running with the given keys.dat on port
# 6713 and expose send and receive functions
import xmlrpc.client
bitmessage = xmlrpc.client.ServerProxy('http://admin:123@127.0.0.1:6713')

# UTF-8 to base64 and back
from base64 import b64encode, b64decode
def b64enc(s): return b64encode(bytes(s, 'utf-8')).decode('utf-8')
def b64dec(b): return b64decode(b).decode('utf-8')

# Send message to chan
from json import dumps as jsdumps
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

def close(): pass
