#!/usr/bin/python3

def listen(filter):
    return []

def propose(filter):
    return True

def offer(tx):
    return True

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
server = SimpleXMLRPCServer(("127.0.0.1", 6712), requestHandler=SimpleXMLRPCRequestHandler)
server.register_introspection_functions()

server.register_function(listen, 'listen')
server.register_function(propose, 'propose')
server.register_function(offer, 'offer')

server.serve_forever()
