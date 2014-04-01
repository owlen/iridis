#!/usr/bin/python3

def getvoutcolor(vout):
    return { 'color': 'gold', 'amount': 1 }

def makeconversion(color, amount1, key, vouts, amount2):
    return 'tx'

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
server = SimpleXMLRPCServer(("127.0.0.1", 6711), requestHandler=SimpleXMLRPCRequestHandler)
server.register_introspection_functions()

server.register_function(getvoutcolor, 'getvoutcolor')
server.register_function(makeconversion, 'makeconversion')

server.serve_forever()
