#!/usr/bin/python3

def getvoutcolor(vout):
    return { 'color': 'gold', 'amount': 1 }

def makeconversion(sieve):
    return { 'hex': 'tx' }

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
server = SimpleJSONRPCServer(('127.0.0.1', 6711))
server.register_introspection_functions()
server.register_function(getvoutcolor, 'getvoutcolor')
server.register_function(makeconversion, 'makeconversion')
print('Serving JSON on 6711')
try:
    server.serve_forever()
except KeyboardInterrupt:
    from sys import exit
    exit(0)
