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
def send(subject, message):
    if not type(message) is str: message = jsdumps(message)
    subject, message = map(b64enc, (subject, message))
    return bitmessage.sendMessage(toaddress, fromaddress, subject, message)

# Get a list of all new messages
from json import loads as jsloads
def receive():
    messages = []
    inbox = jsloads(bitmessage.getAllInboxMessages())['inboxMessages']
    for msgid in (m['msgid'] for m in inbox):
        message = jsloads(bitmessage.getInboxMessageByID(msgid))['inboxMessage'][0]
        subject, message = map(b64dec, (message['subject'], message['message']))
        messages.append({'subject': subject, 'message': message})
        bitmessage.trashMessage(msgid)
    return messages

# Serve RPC
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
server = SimpleXMLRPCServer(("127.0.0.1", 6712), requestHandler=SimpleXMLRPCRequestHandler)
server.register_introspection_functions()

server.register_function(send, 'send')
server.register_function(receive, 'receive')

try:
    server.serve_forever()
except KeyboardInterrupt:
    from sys import exit
    exit(0)
