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
from subprocess import Popen, PIPE
from os import path
curpath = path.dirname(path.abspath(__file__))
bitcoindprocess = Popen(('bitcoind', '-conf=' + curpath + '/bitcoin.conf'), stdout=PIPE)

# Connect to its JSON-RPC server
import jsonrpclib
bitcoind = jsonrpclib.Server('http://user:pass@127.0.0.1:18332')

# Implement required functionality
def signrawtransaction(rawtx, txinputs, privatekeys):
    tx = bitcoind.signrawtransaction(rawtx, txinputs, privatekeys)
    if tx['complete']:
        tx.update({
            'txid': bitcoind.sendrawtransaction(tx['hex'])
        })
    return tx

def close():
    bitcoind.stop()
    # FIXME should be a way to use 'communicate' here, but for now a delay will suffice.
    from time import sleep
    sleep(3)
    bitcoindprocess.terminate()
