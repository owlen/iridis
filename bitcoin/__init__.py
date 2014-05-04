#!/usr/bin/python3

# Connect to a bitcoind RPC server on port 18332 and expose signrawtransaction and sendrawtransaction

# Make sure the port is available
port = 18332
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if 0 == sock.connect_ex(('localhost', port)):
    sock.close()
    raise Exception("port %d is in use, aborting" % (port,))

# Run bitcoind
from subprocess import Popen, DEVNULL
from os import path
curpath = path.dirname(path.abspath(__file__))
bitcoindprocess = Popen(('bitcoind', '-conf=' + curpath + '/bitcoin.conf'), stdout=DEVNULL)

# Connect to its JSON-RPC server
import jsonrpclib
bitcoind = jsonrpclib.Server('http://user:pass@127.0.0.1:18332')

def signrawtransaction(rawtx, txinputs, privatekeys):
    return bitcoind.signrawtransaction(rawtx, txinputs, privatekeys)

def sendrawtransaction(rawtx):
    return bitcoind.sendrawtransaction(rawtx)

# Implement required functionality
def close():
    bitcoind.stop()
    from time import sleep
    sleep(3)
    bitcoindprocess.terminate()
