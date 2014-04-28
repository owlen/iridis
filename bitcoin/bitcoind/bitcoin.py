#!/usr/bin/python3

import jsonrpclib
btcserver = jsonrpclib.Server('http://user:pass@127.0.0.1:18332')

def getrawtransaction(txid): return btcserver.getrawtransaction(txid)
def decoderawtransaction(rawtx): return btcserver.decoderawtransaction(rawtx)
def signrawtransaction(rawtx, txinputs, privatekeys): return signrawtransaction(rawtx, txinputs, privatekeys)
def sendrawtransaction(rawtx): return btcserver.sendrawtransaction(rawtx)

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
server = SimpleJSONRPCServer(('127.0.0.1', 6714))
server.register_introspection_functions()
server.register_function(getrawtransaction, 'getrawtransaction')
server.register_function(decoderawtransaction, 'decoderawtransaction')
server.register_function(signrawtransaction, 'signrawtransaction')
server.register_function(sendrawtransaction, 'sendrawtransaction')
print('Serving JSON on 6714')
try:
    server.serve_forever()
except KeyboardInterrupt:
    from sys import exit
    exit(0)
