#!/usr/bin/python3

# Connect to a fully indexed bitcoind server running with the given bitcoin.conf
# on port 18332 and expose getscriptpubkey and signrawtransaction

import jsonrpclib
bitcoind = jsonrpclib.Server('http://user:pass@127.0.0.1:18332')

def getscriptpubkey(txo):
    tx = bitcoind.getrawtransaction(txo[0])
    tx = bitcoind.decoderawtransaction(tx)
    return tx['vout'][txo[1]]['scriptPubKey']['hex']

def signrawtransaction(rawtx, txinputs, privatekeys):
    tx = bitcoind.signrawtransaction(rawtx, txinputs, privatekeys)
    return tx

def close(): pass
