#!/usr/bin/python3

# Connect to bitmessage - user and pass configured with:
# https://github.com/Dokument/PyBitmessage-Daemon
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
            messages.append({'subject': subject, 'body': jsloads(body), 'fromaddress': fromaddress})
        bitmessage.trashMessage(msgid)
    if len(messages) > 0: print('transfered incoming messages: ', messages)
    return messages

# Serve RPC
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
server = SimpleJSONRPCServer(('127.0.0.1', 6712))
server.register_introspection_functions()
server.register_function(send, 'send')
server.register_function(receive, 'receive')
print('Serving JSON on 6712')
try:
    server.serve_forever()
except KeyboardInterrupt:
    from sys import exit
    exit(0)
